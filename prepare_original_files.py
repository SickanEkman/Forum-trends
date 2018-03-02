import original_filenames
import json
import collections
import os.path


def create_work_files(og_file):
    """
    :param og_file: an original forum json-file with no modifications
    :return: send a dict for each file to function "separate_each_month"
    """
    data = collections.defaultdict(list)
    with open(og_file, "r") as fin:
        og_forum = json.load(fin)
        for dialogs in og_forum["dialogs"]:
            dialog_text = dialogs["content_text"]
            dialog_text = dialog_text.replace("\n", " ")
            dialog_text = dialog_text.replace("  ", " ")
            dialog_date = dialogs["meta"]["published"]
            dialog_date = dialog_date[0:7]
            data[dialog_date].append(dialog_text)
            for comments in dialogs["comments"]:
                comment_text = comments["content_text"]
                comment_text = comment_text.replace("\n", " ")
                comment_text = comment_text.replace("  ", " ")
                comment_date = comments["meta"]["published"]
                comment_date = comment_date[0:7]
                data[comment_date].append(comment_text)
    fin.close()
    separate_each_month(data, og_file[6])


def separate_each_month(data_dict, file_name):
    """
    :param data_dict: k=date, v=list with texts
    :param file_name: the identifier from original files, example= "a", "k", ...
    :return: files for each month, with all text joined, example path: "m_months/m_2016-01.txt"
    """
    subdir = file_name + "_months"
    try:
        os.mkdir(subdir)
    except FileExistsError:
        print("Directory '%s' already exists." % subdir)
    for date, texts in data_dict.items():
        big_str = " ".join(texts)
        outfile_name = file_name + "_" + date + ".txt"
        with open(os.path.join(subdir, outfile_name), "w") as fout:
            fout.write(big_str)
        fout.close()


if __name__ == "__main__":
    forums = original_filenames.forums
    for forum in forums:
        create_work_files(forum)
