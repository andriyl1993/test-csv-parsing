import csv
import requests
import io


def prepare_data(data):
    return [item for item in data]


def main(data_url, enrichment_url):
    persons_content = requests.get(data_url).content
    enrichment_content = requests.get(enrichment_url).content
    
    enrichment_data = list(csv.reader(io.StringIO(enrichment_content.decode())))
    new_data = []
    for persons_line in csv.reader(io.StringIO(persons_content.decode())):
        if not new_data:
            new_data.append(prepare_data(enrichment_data[0]))
            continue

        new_data_line = persons_line[:4]

        for enrichment_line in enrichment_data[1:]:
            if all(item == persons_line[i] for i, item in enumerate(enrichment_line[:4])):
                new_data_line.append(enrichment_line[4])
                break
        else:
            new_data_line.append("")

        new_data.append(prepare_data(new_data_line))

    with open("file.csv", "r+") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(new_data)

        f.seek(0)
        return f.read()


data_url = "https://auto-clinvar-gal-test.s3.amazonaws.com/data.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAR2AZSYRQVFJLQULI%2F20241120%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241120T103115Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Security-Token=FwoGZXIvYXdzEAQaDF06ZEZYIz%2Bh06QO8CLsAZNuCtwGPgvZoeHY4YnnNfa2Ag05VcBIQqfCZXtJQTZYXrjVuxqNTgRqRShQEi4IV5UDbe%2BPs6WClNYkBuqfoG%2FZvnukZP6LVPIzwkQxiMT%2B57erVgH1PHUGo7zn0SbEnuB2Hq%2F%2FgM86thpew6wSXNx%2F0GfU98tsoKeOMDvPcsFTNH7TXEIVS7AVaG7W7o%2FA2%2FgQbhAF4BPITTVxtwHeaQ8U89FL90GlT82JDc1hCN2%2BzLtlQsOY5BgM%2BJxfufyR23Zz%2FShA5YhqHJIlaY3tud0hdSVffBxbjx3aFgL8c%2Bf70RaU8JPeNNSX%2Fvd8KOn09rkGMitBfook0H5zqwPtoaIhp9MfXDGRoGqqjumH8yNaiEPAAhr4JHD6idXxOy9Q&X-Amz-Signature=6804667bf35d894b285e88e775a7c95236bd4bff749805817629d32c7703c66f"
enrichment_url = "https://auto-clinvar-gal-test.s3.amazonaws.com/enrichment.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAR2AZSYRQVFJLQULI%2F20241120%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241120T103124Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Security-Token=FwoGZXIvYXdzEAQaDF06ZEZYIz%2Bh06QO8CLsAZNuCtwGPgvZoeHY4YnnNfa2Ag05VcBIQqfCZXtJQTZYXrjVuxqNTgRqRShQEi4IV5UDbe%2BPs6WClNYkBuqfoG%2FZvnukZP6LVPIzwkQxiMT%2B57erVgH1PHUGo7zn0SbEnuB2Hq%2F%2FgM86thpew6wSXNx%2F0GfU98tsoKeOMDvPcsFTNH7TXEIVS7AVaG7W7o%2FA2%2FgQbhAF4BPITTVxtwHeaQ8U89FL90GlT82JDc1hCN2%2BzLtlQsOY5BgM%2BJxfufyR23Zz%2FShA5YhqHJIlaY3tud0hdSVffBxbjx3aFgL8c%2Bf70RaU8JPeNNSX%2Fvd8KOn09rkGMitBfook0H5zqwPtoaIhp9MfXDGRoGqqjumH8yNaiEPAAhr4JHD6idXxOy9Q&X-Amz-Signature=e752fe2570ee177b8572f0fdbdb61bf6b171ad34abb09a35bdb70d31d11a47f1"

if __name__ == "__main__":
    main(
        data_url=data_url,
        enrichment_url=enrichment_url,
    )