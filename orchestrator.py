import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description='Orchestrate SageMaker Training and Inference')
    parser.add_argument('--mode', type=str, choices=['train', 'inference', 'register'], required=True,
                        help='Mode to run the orchestrator: train or inference')
    args = parser.parse_args()

    if args.mode == 'train':
        subprocess.run(["python", "train_orchestrator.py"])
    elif args.mode == 'inference':
        subprocess.run(["python", "inference_orchestrator.py"])
    elif args.mode == 'register':
        subprocess.run(["python", "register_model_orchestrator.py"])

if __name__ == "__main__":
    main()