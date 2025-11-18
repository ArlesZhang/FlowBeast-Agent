import pandas as pd

def run_workflow():
    df = pd.read_csv("")
    df = df.query("")
    df.to_parquet("", index=False)
    print("Saved to ")
    print("Workflow completed!")
if __name__ == "__main__":
    run_workflow()