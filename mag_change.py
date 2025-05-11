import os
import pandas as pd

def compare_stats(pre_df, post_df, folder_name):
    # Find common columns by name
    common_columns = pre_df.columns.intersection(post_df.columns)

    # Compute statistics
    comparison = []
    for col in common_columns:
        pre_mean = pre_df[col].abs().mean()
        pre_std = pre_df[col].std()
        post_mean = post_df[col].abs().mean()
        post_std = post_df[col].std()
        mean_diff = post_mean - pre_mean
        std_diff = post_std - pre_std
        comparison.append((col, pre_mean, post_mean, mean_diff, pre_std, post_std, std_diff))

    # Format table
    lines = []
    header = f"{'Column':<30} {'Pre Mean':>10} {'Post Mean':>12} {'Mean Diff':>12} {'Pre Std':>10} {'Post Std':>12} {'Std Diff':>10}"
    lines.append(header)
    lines.append("-" * len(header))
    for row in comparison:
        col, pre_mean, post_mean, mean_diff, pre_std, post_std, std_diff = row
        lines.append(f"{col:<30} {pre_mean:10.4f} {post_mean:12.4f} {mean_diff:12.4f} {pre_std:10.4f} {post_std:12.4f} {std_diff:10.4f}")

    # Write per-folder file
    out_path = os.path.join(folder_name, "comparison.txt")
    with open(out_path, "w") as f:
        f.write(f"Comparison for {os.path.basename(folder_name)}\n\n")
        f.write("\n".join(lines))

    return f"\nComparison for {os.path.basename(folder_name)}\n" + "\n".join(lines) + "\n"

def process_all_folders(base_dir="."):
    summary = []
    for folder in sorted(os.listdir(base_dir)):
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path):
            try:
                files = os.listdir(folder_path)
                pre_file = next(f for f in files if f.endswith(".xlsx") and not f.endswith("p.xlsx"))
                post_file = next(f for f in files if f.endswith("p.xlsx"))

                pre_df = pd.read_excel(os.path.join(folder_path, pre_file))
                post_df = pd.read_excel(os.path.join(folder_path, post_file))

                summary_text = compare_stats(pre_df, post_df, folder_path)
                summary.append(summary_text)

            except Exception as e:
                print(f"❌ Skipped {folder_path}: {e}")

    # Write combined summary
    with open("summary.txt", "w") as f:
        f.write("\n".join(summary))
    print("✅ Summary written to summary.txt")

if __name__ == "__main__":
    process_all_folders()
