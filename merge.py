import json


def merge_json(existing_file, new_file):
    if existing_file.exists():
        with existing_file.open('r') as infile:
            try:
                data = json.load(infile)
            except json.decoder.JSONDecodeError:
                print("invalid existing json file, couldn't update")
                return
    else:
        # TODO write new file to save location
        print('no existing history file')
        return

    if new_file.exists():
        with new_file.open('r') as infile:
            try:
                new_data = json.load(infile)
            except json.decoder.JSONDecodeError:
                print("invalid new json file, couldn't update")
                return
    else:
        print('new file does not exist')
        return

    combined_data = data.copy()
    for day in new_data.keys():
        if day in combined_data:
            for activity in new_data[day].keys():
                if activity in combined_data[day]:
                    combined_data[day][activity] += new_data[day][activity]
                else:
                    combined_data[day][activity] = new_data[day][activity]

        else:
            combined_data[day] = new_data[day].copy()

    with existing_file.open('w') as f:
        json.dump(combined_data, f, indent=4)
