from pathlib import Path
import argparse
import wave


def get_sample_rate(wav_path: Path):
    try:
        with wave.open(str(wav_path), "rb") as wav:
            return wav.getframerate()
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(description="DiffSinger Dataset Checker")
    parser.add_argument(
        "--dataset",
        required=True,
        help="Dataset folder path"
    )
    args = parser.parse_args()

    dataset = Path(args.dataset)

    if not dataset.exists():
        print(f"❌ Dataset not found: {dataset}")
        return

    wavs = sorted(dataset.glob("*.wav"))
    labs = sorted(dataset.glob("*.lab"))

    print("=" * 50)
    print("DiffSinger Dataset Checker")
    print("=" * 50)

    print(f"WAV files : {len(wavs)}")
    print(f"LAB files : {len(labs)}")

    failed = False

    if len(wavs) != len(labs):
        print("❌ Number of WAV and LAB files does not match.")
        failed = True

    wav_names = {x.stem for x in wavs}
    lab_names = {x.stem for x in labs}

    missing_lab = sorted(wav_names - lab_names)
    missing_wav = sorted(lab_names - wav_names)

    if missing_lab:
        print("\nMissing LAB:")
        for name in missing_lab:
            print(" -", name)

    if missing_wav:
        print("\nMissing WAV:")
        for name in missing_wav:
            print(" -", name)

    dictionary = dataset / "dictionary-ja.txt"

    if dictionary.exists():
        print("\nDictionary : OK")
    else:
        print("\n❌ dictionary-ja.txt not found")
        failed = True

    print("\nSample Rates")

    rates = {}

    for wav in wavs:
        sr = get_sample_rate(wav)
        rates.setdefault(sr, 0)
        rates[sr] += 1

    for sr, count in sorted(rates.items()):
        print(f"{sr} Hz : {count}")

    if len(rates) > 1:
        print("\n⚠ Multiple sample rates detected.")

    print("\n" + "=" * 50)

    if failed:
        print("❌ DATASET CHECK FAILED")
    else:
        print("✅ DATASET CHECK PASSED")

    print("=" * 50)


if __name__ == "__main__":
    main()
