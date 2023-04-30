from data_fetcher import fetch_data

NEW_ANIMALS_DATA_HTML = 'animals.html'
ANIMALS_DATA_HTML = 'animals_template.html'


def get_user_input():
    """ PROMPTS USER FOR INPUT"""
    animal_name = input("Enter a name for an animal: ")
    return animal_name.strip()


def process_animal_data(animal_data):
    """GETS ANIMAL DATA AND RETURNS LIST OF DICTIONARIES OF ANIMAL INFO
    [{'NAME':...}, {'LOCATION':...}, ...]"""
    # RETURNS NONE IF ANIMAL NOT FOUND IN API
    if not animal_data:
        return None

    animals_data_processed = []
    for index in range(len(animal_data)):
        animal_type = animal_diet = False  # INITIALIZING BOTH VARIABLES TO FALSE

        animal_name = animal_data[index]['name']
        animal_location = animal_data[index]['locations'][0]
        animal_characteristics = animal_data[index]['characteristics']
        if 'type' in animal_characteristics:
            animal_type = animal_data[index]['characteristics']['type']
        if 'diet' in animal_characteristics:
            animal_diet = animal_data[index]['characteristics']['diet']

        if animal_type and animal_diet:
            animals_data_processed.append(
                dict(Name=animal_name, Diet=animal_diet,
                     Location=animal_location, Type=animal_type))
            continue
        if animal_type:
            animals_data_processed.append(
                dict(Name=animal_name, Location=animal_location,
                     Type=animal_type))
            continue
        if animal_diet:
            animals_data_processed.append(
                dict(Name=animal_name, Location=animal_location,
                     Diet=animal_diet))
            continue
    return animals_data_processed


def serialize_animal_data(animal_data, animal_name):
    """GETS ANIMAL DATA AND RETURNS A SERIALIZED OUTPUT FOR HTML"""
    output = '<li class="cards__item">'
    if animal_data is None:
        output += f"\n  <h2>The animal \"{animal_name}\" doesn't exist.</h2>"
    else:
        for animal in animal_data:
            for animal_detail in animal:
                if animal_detail == 'Name':
                    output += f"\n<div class = 'card__title' >" \
                              f"{animal[animal_detail]}</div>\n"
                else:
                    output += f"<p class = 'card__text'><strong" \
                              f">{animal_detail}:</strong>" \
                              f" {animal[animal_detail]}</p>\n"
            output += '</li>\n\n<li class="cards__item">'
    # REMOVES OPENING Li TAG TO PREVENT CREATING AN EMPTY CARD
    if output.endswith('<li class="cards__item">'):
        return output.removesuffix('\n<li class="cards__item">')


def read_html_file(filepath):
    """READ HTML FILE AND RETURNS HTML CONTENT"""
    with open(filepath, 'r') as f:
        html_file = f.read()
        return html_file


def replace_file_content(original_content, replacement):
    """GETS ORIGINAL HTML CONTENT AND REPLACES PARTS OF CONTENTS WITH A
    REPLACEMENT"""
    return original_content.replace('__REPLACE_ANIMALS_INFO__', replacement)


def write_to_html_file(filepath, new_content):
    """WRITES NEW CONTENT TO NEW HTML FILE"""
    with open(filepath, 'w') as f:
        f.write(new_content)
        print(f'Website was successfully generated to the file {filepath}')


def main():
    """MAIN: CALLS OTHER FUNCTIONS"""
    animal_name = get_user_input()
    # LOAD DATA FROM JSON FILE
    animal_data = fetch_data(animal_name)
    # PROCESS DATA FOR SERIALIZATION
    animal_data_processed = process_animal_data(animal_data)
    # SERIALIZE DATA
    new_content = serialize_animal_data(animal_data_processed, animal_name)
    # READ HTML CONTENT FROM HTML FILE
    html_file = read_html_file(ANIMALS_DATA_HTML)
    # REPLACE HTML CONTENT WITH SERIALIZED DATA
    new_html_content = replace_file_content(html_file, new_content)
    # WRITE CONTENT TO NEW HTML FILE
    write_to_html_file(NEW_ANIMALS_DATA_HTML, new_html_content)


if __name__ == '__main__':
    main()
