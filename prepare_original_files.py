import original_filenames
import json
import collections
import os.path


def create_work_files(og_file):
    """
    Takes an original forum file, saves to dict:
    * Text in original forum post
    * Text in comments
    * Date with format YYYY-MM
    Save format: {"2016-01": ["Post text","Another text"] "2015-05":, [...]}
    :param og_file: the original forum json-file with no modifications
    :return: writes dict to output file, example names: data_a.json, data_k.json
    """
    data = collections.defaultdict(list)
    with open(og_file, "r") as fin:
        forum = json.load(fin)
        for dialogs in forum["dialogs"]:
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
    outfile_name = "data_" + og_file[6] + ".json"
    with open(outfile_name, "w") as fout:
        json.dump(data, fout)
    fout.close()


def separate_each_month(mod_file):
    """
    opens modified file containing a specific forum and saves every month within the forum to separate file.
    :param mod_file: modified forum file with date as dict key and list with texts as value
    :return: files for each month, with all text joined, example path: "m_months/m_2016-01.txt"
    """
    subdir = mod_file[5] + "_months"
    try:
        os.mkdir(subdir)
    except FileExistsError:
        print("Directory '%s' already exists." % mod_file)
    with open(mod_file, "r") as fin:
        forum_text = json.load(fin)
        for date, texts in forum_text.items():
            big_str = " ".join(texts)
            outfile_name = mod_file[5] + "_" + date + ".txt"
            with open(os.path.join(subdir, outfile_name), "w") as fout:
                fout.write(big_str)
            fout.close()
    fin.close()


def mod_og_files():
    forums = original_filenames.forums  # haven't tested program after moving file names to separate file,
    # change if needed
    for forum in forums:
        create_work_files(forum)


def mod_work_files():
    data_files = ["data_a.json",
                  "data_c.json",
                  "data_k.json",
                  "data_l.json",
                  "data_m.json",
                  "data_s.json"]
    for data_file in data_files:
        separate_each_month(data_file)
