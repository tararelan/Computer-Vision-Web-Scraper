import json
import pandas as pd
import yaml
import os


def annot_yolo(annot_file, cats):
    df_ann = pd.read_csv(annot_file)

    df_ann["int_category"] = df_ann["category"].apply(lambda x: cats.index(x) if x in cats else None)
    df_ann["box_center_w"] = df_ann["box_left"] + df_ann["box_width"] / 2
    df_ann["box_center_h"] = df_ann["box_top"] + df_ann["box_height"] / 2

    # scale box dimensions by image dimensions
    df_ann["box_center_w"] = df_ann["box_center_w"] / df_ann["img_width"]
    df_ann["box_center_h"] = df_ann["box_center_h"] / df_ann["img_height"]
    df_ann["box_width"] = df_ann["box_width"] / df_ann["img_width"]
    df_ann["box_height"] = df_ann["box_height"] / df_ann["img_height"]

    return df_ann


def save_annots_to_csv(directory, df_local):
    unique_images = df_local["img_file"].unique()

    for image_file in unique_images:
        df_single_img_annots = df_local.loc[df_local.img_file == image_file]
        annot_txt_file = image_file.split(".")[0] + ".txt"
        destination = f"{directory}/{annot_txt_file}"

        df_single_img_annots.to_csv(
            destination,
            index=False,
            header=False,
            sep=" ",
            float_format="%.4f",
            columns=[
                "int_category",
                "box_center_w",
                "box_center_h",
                "box_width",
                "box_height",
            ],
        )


def get_cats(yaml_file):
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
        labels = data['names']

    return labels


def main():
    with open("input.json") as fjson:
        input_dict = json.load(fjson)

    job_id = input_dict["job_id"]
    gt_annot_file = input_dict["ground_truth_annotations"]
    yolo_output = input_dict["yolo_output_dir"]

    yaml_file = "data.yaml"
    categories = get_cats(yaml_file)
    print("\n labels used in Ground Truth job: ")
    print(categories, "\n")

    output_dir = f"{job_id}/{yolo_output}"
    os.makedirs(output_dir, exist_ok=True)
    print(f"annotation files saved in = ", output_dir)

    df_annot = annot_yolo(gt_annot_file, categories)
    save_annots_to_csv(output_dir, df_annot)


if __name__ == "__main__":
    main()