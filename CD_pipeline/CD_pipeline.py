import shutil

# Simulate delivery from staging to mirror
def deliver_artifact(src, dest):
    shutil.copy(src, dest)
    print(f"Delivered {src} → {dest}")

deliver_artifact("dev/build/app_c.zip", "test/mirror-data/app_c.zip")
deliver_artifact("dev/build/app_c.zip", "prod/mirror-data/app_c.zip")
