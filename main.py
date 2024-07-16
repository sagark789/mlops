import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, choices=['train', 'inference'], required=True, help='Mode to run: train or inference')
    args = parser.parse_args()

    if args.mode == 'train':
        subprocess.run(['python', '/opt/ml/code/train.py'])
    elif args.mode == 'inference':
        subprocess.run(['python', '/opt/ml/code/inference.py'])  # Placeholder for inference script

if __name__ == '__main__':
    main()
