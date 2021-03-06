#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import pathlib
import subprocess

from zimscraperlib.constants import SCRAPER
from zimscraperlib.zim import make_zim_file


def test_ziminfo_defaults(ziminfo):
    assert ziminfo.language == "eng"
    assert ziminfo.title == "my title"
    assert ziminfo.description == "my zim description"
    assert ziminfo.creator == "unknown"
    assert ziminfo.publisher == "kiwix"
    assert ziminfo.name == "test-zim"
    assert ziminfo.tags == []
    assert ziminfo.homepage == "home.html"
    assert ziminfo.favicon == "favicon.png"
    assert ziminfo.scraper == SCRAPER


def test_updating_values(ziminfo):
    updates = {"language": "fra", "title": "new title"}
    ziminfo.update(**updates)
    for k, v in updates.items():
        assert getattr(ziminfo, k) == v


def test_zimfriterfs_args(ziminfo):

    zwfs = ziminfo.to_zimwriterfs_args()
    assert len(zwfs) == 20
    options_map = [
        ("welcome", "homepage"),
        ("favicon", "favicon"),
        ("language", "language"),
        ("title", "title"),
        ("description", "description"),
        ("creator", "creator"),
        ("publisher", "publisher"),
        ("name", "name"),
        ("tags", "tags"),
        ("scraper", "scraper"),
    ]

    for index, option_data in enumerate(options_map):
        option, attr = option_data
        arg_index = index * 2
        assert zwfs[arg_index] == f"--{option}"
        if option != "tags":
            assert zwfs[arg_index + 1] == getattr(ziminfo, attr)
        else:
            assert zwfs[arg_index + 1] == ";".join(getattr(ziminfo, attr))


def test_zimwriterfs_command(monkeypatch, ziminfo):

    build_dir = pathlib.Path("build")
    output_dir = pathlib.Path("output")
    zim_fname = f"{ziminfo.name}.zim"

    def mock_subprocess_run(args, **kwargs):
        assert len(args) == 24
        assert args[-1].endswith(".zim")
        assert args[-1] == str(output_dir.joinpath(zim_fname))
        assert args[-2] == str(build_dir)
        return subprocess.CompletedProcess(args=args, returncode=0)

    monkeypatch.setattr(subprocess, "run", mock_subprocess_run)
    make_zim_file(build_dir, output_dir, zim_fname, ziminfo)
