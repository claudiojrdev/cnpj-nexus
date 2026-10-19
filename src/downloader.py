import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom


url = "https://arquivos.receitafederal.gov.br/public.php/webdav"
token = "YggdBLfdninEJX9"

def propfind(url: str, path: str) -> ET.Element:
    """PROPFIND in url/path"""
    url = f"{url}/{path}".rstrip("/")
    response = requests.request(
        "PROPFIND",
        url,
        auth=(token,""),
        headers={"Depth":"1"}
    )
    response.raise_for_status()

    write_xml_doc(response.content)

    return ET.fromstring(response.content)

def write_xml_doc(xml_str) -> str:
    """Write xml string in a pretty format content in xml"""
    dom = minidom.parseString(xml_str)
    dom = dom.toprettyxml(indent="    ")
    
    write_doc(dom,"./xml-content.xml")

def write_doc(content,file_path):
    """Write content in a file path"""
    arquivo = open(file_path,mode="w",encoding="utf-8")
    arquivo.write(str(content))
    arquivo.close()


def get_available_resources(url: str, path: str) -> list[str]:
    print(f"Getting available resources from {url}/{path}:")

    root = propfind(url, path)

    namespace = {"d": "DAV:"}
    available_resources_paths = []
    for response in root.findall("d:response", namespace):
        href = response.find("d:href", namespace)

        if href is not None:
            available_resources_paths.append(href.text)
    return available_resources_paths


def download_by_path(file_url,filename:str):
    response = requests.get(
        url=file_url,
        auth=(token,"")
    )
    response.raise_for_status()

    with open(filename,"wb") as file:
        file.write(response.content)


def download_all_from_path(url,path) -> None:
    available_resources_paths = get_available_resources(url,path)
    for resource_path in available_resources_paths[1:]:
        # filename = resource_path.split("/")[-1]
        file_path = f"./data/{resource_path.split("/")[-2]}/{resource_path.split("/")[-1]}"
        full_url = f"https://arquivos.receitafederal.gov.br{resource_path}"
        download_by_path(full_url,file_path)

# available_resources_paths = get_available_resources(url,"")
# available_resources_paths = get_available_resources(url,"2026-08/Motivos.zip")
# for resource in available_resources_paths:
#     print(resource)

download_all_from_path(url,"2026-08")
# print(get_available_resources(url,"2026-08/Motivos.zip"))
# download_by_path(url,"2026-08/Motivos.zip","Motivos.zip")

