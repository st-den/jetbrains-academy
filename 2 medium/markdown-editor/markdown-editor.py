markdown, addition = "", ""

while choice := input("Choose a formatter: "):
    match choice:
        case "plain":
            addition = input("Text: ")

        case "bold":
            addition = f"**{input('Text: ')}**"

        case "italic":
            addition = f"*{input('Text: ')}*"

        case "header":
            while (lvl := int(input("Level: "))) not in range(1, 7):
                print("The level should be within the range of 1 to 6")
            addition = f"{'#' * lvl} {input('Text: ')}\n"

        case "link":
            addition = f"[{input('Label: ')}]({input('URL: ')})"

        case "inline-code":
            addition = f"`{input('Text: ')}`"

        case "new-line":
            addition = "\n"

        case "ordered-list":
            while not (n_rows := int(input("Number of rows: "))) > 0:
                print("The number of rows should be greater than zero")
            addition = "".join(
                [f"{i + 1}. {input(f'Row #{i + 1}: ')}\n" for i in range(n_rows)]
            )

        case "unordered-list":
            while not (n_rows := int(input("Number of rows: "))) > 0:
                print("The number of rows should be greater than zero")
            addition = "".join(
                [f"* {input(f'Row #{i + 1}: ')}\n" for i in range(n_rows)]
            )

        case "!help":
            print(
                "Available formatters: plain bold italic header link inline-code ordered-list unordered-list new-line"
            )
            print("Special commands: !help !done")

        case "!done":
            with open("output.md", "w") as f:
                f.write(markdown)
            break

        case _:
            print("Unknown formatting type or command")

    if addition:
        markdown += addition
        print(markdown)
