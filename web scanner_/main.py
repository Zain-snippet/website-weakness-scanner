from pipeline import run_scan

def main():
    print("=== Smart Web App Weakness Finder (Demo) ===\n")

    while True:
        url = input("Enter URL to scan (or type 'exit' to quit): ").strip()
        if url.lower() == "exit":
            print("\n[INFO] Exiting scanner. Goodbye!")
            break

        if not url:
            url = "http://127.0.0.1:5000"  # fallback demo app

        print(f"\n[INFO] Scanning: {url}\nPlease wait...\n")
        print("-" * 40)  # visual separation

        report = run_scan(url)
        print(report)
        print("-" * 40)  # end separation

        input("\nPress Enter to continue...")  # ensures user sees the report

if __name__ == "__main__":
    main()