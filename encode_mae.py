from argparse import ArgumentParser
from pathlib import Path
from glob import glob

import librosa
import numpy as np
import torch
from tqdm import tqdm
from encodec import EncodecModel

from encodecmae import load_model


parser = ArgumentParser()
parser.add_argument("audio_dir", type=Path)
parser.add_argument("embeddings_dir", type=Path)
parser.add_argument("--model-size", type=str, default="base")
parser.add_argument("--format", type=str, default="wav", choices=["wav", "mp3"])
parser.add_argument("--device", type=str, default="cuda:0")

args = parser.parse_args()

device = args.device


ecmae = load_model("base", device=device)

# ec = EncodecModel.encodec_model_24khz()
# ec.to(device)

glob_pattern = str(args.audio_dir / "**" / f"*.{args.format}")
print(glob_pattern)
audio_files = glob(glob_pattern, recursive=True)

for audio_file in tqdm(audio_files):
    audio_file = Path(audio_file)

    output_path = (
        args.embeddings_dir / args.model_size / audio_file.parent.name / audio_file.stem
    ).with_suffix(".npy")

    if output_path.exists():
        continue

    xorig, fs = librosa.core.load(audio_file, sr=24000)
    n_patches = xorig.shape[0] // (4 * fs)
    xorig = xorig[: n_patches * 4 * fs].reshape(-1, 4 * fs)

    x = {
        "wav": torch.from_numpy(xorig).to(device=device, dtype=ecmae.dtype),
        "wav_lens": torch.tensor(
            [
                xorig.shape[1],
            ]
            * xorig.shape[0],
            device=device,
        ),
    }
    ecmae.visible_encoder.compile = False

    with torch.no_grad():
        ecmae.encode_wav(x)
        ecmae.mask(x, ignore_mask=True)
        ecmae.encode_visible(x)
        ecmae_features = x["visible_embeddings"]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(output_path, ecmae_features.detach().cpu().numpy())
