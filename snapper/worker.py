import logging
import os
import shutil
from pathlib import Path
from uuid import uuid4

from jinja2 import Environment, PackageLoader
from snapper.web_driver import WebDriver

env = Environment(autoescape=True,
                  loader=PackageLoader('snapper', 'templates'))


def copy_template(task):
    css_output_path = Path(task.output_path) / "css"
    js_output_path = Path(task.output_path) / "js"
    images_output_path = Path(task.output_path) / "images"

    os.makedirs(css_output_path)
    os.makedirs(js_output_path)
    os.makedirs(images_output_path)

    css_template_path = Path(__file__).parent / "templates" / "css"
    js_template_path = Path(__file__).parent / "templates" / "js"
    shutil.copyfile(
        css_template_path / "materialize.min.css",
        css_output_path / "materialize.min.css"
    )
    shutil.copyfile(
        js_template_path / "jquery.min.js",
        js_output_path / "jquery.min.js"
    )
    shutil.copyfile(
        js_template_path / "materialize.min.js",
        js_output_path / "materialize.min.js"
    )


def host_worker(url_id, task):
    with WebDriver(task.user_agent, task.chrome_binary, task.timeout) as web_driver:
        filename = Path(task.output_path) / "images" / (str(uuid4()) + ".png")

        host = task.urls[url_id]
        if not host.startswith("https://") and not host.startswith("http://"):
            host = "http://" + host

        logging.debug("Fetching %s", host)
        if WebDriver.host_reachable(host, task.timeout) and web_driver.save_image(host, str(filename)):
            return task.urls[url_id], str(filename)
        else:
            logging.debug("%s is unreachable or timed out", host)
            return task.urls[url_id], None


def finish_task(urls_to_filenames, task, output_paths_format):
    task.result.update({
        _: output_paths_format.format(filename) if filename else None
        for _, filename in urls_to_filenames
    })

    # absolute path to relative path
    urls_to_filenames = [
        (_, os.path.relpath(filename, task.output_path))
        for _, filename in urls_to_filenames
        if filename
    ]

    sets_of_six = list(zip(*[iter(urls_to_filenames)]*6))
    sets_of_six.append(urls_to_filenames[len(sets_of_six)*6:])

    template = env.get_template('index.html')
    index_file_path = Path(task.output_path) / "index.html"
    with open(index_file_path, "w") as index_file:
        index_file.write(template.render(sets_of_six=sets_of_six))

    task.result.update({"all": output_paths_format.format(str(index_file_path))})
    task.status = "ready"
