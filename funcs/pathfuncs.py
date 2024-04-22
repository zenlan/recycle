import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
LOG_DIR = os.path.join(ROOT_DIR, "log", "")
DATA_DIR = os.path.join(ROOT_DIR, "dat", "")
OUT_DIR = os.path.join(ROOT_DIR, "out", "")

if not os.path.exists("dat"):
    os.mkdir("dat")
if not os.path.exists("log"):
    os.mkdir("log")
if not os.path.exists("out"):
    os.mkdir("out")
