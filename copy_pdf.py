import shutil
import os

src = "/Users/sunjiaqi/个人项目程序/PersonalKnowledgeBase/raw/研究报告/01-宏观策略/20260402-东吴证券-东吴证券#海外政治：特朗普准备\"TACO\"，但霍尔木兹海峡依旧\"悬而未决\".pdf"
dst = "/Users/sunjiaqi/个人项目程序/PersonalKnowledgeBase/temp_taco.pdf"

# Check if source exists
print(f"Source exists: {os.path.exists(src)}")
print(f"Source is file: {os.path.isfile(src)}")

# Copy the file
shutil.copy2(src, dst)
print(f"File copied to: {dst}")