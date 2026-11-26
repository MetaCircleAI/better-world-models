# How Much Better Can World Models Get by Changing Only the Architecture?

Bangzhe Huang, Ziming Liu · MetaCircle AI · Tsinghua University · Fudan University

**Read the post: [English](https://metacircleai.github.io/better-world-models/) · [中文](https://metacircleai.github.io/better-world-models/zh/)**

![Three world models, only the architecture changes](figures/hero.png)

We took one representative of each common kind of world model and changed nothing but its network architecture:

- **Control:** [SuperMimic](https://arxiv.org/abs/2610.28480) humanoid motion tracking reaches the return of its 3-hour training in 26.6 minutes on one H100.
- **Representation:** a [V-JEPA](https://arxiv.org/abs/2404.08471)-style video encoder on [CLEVRER](https://arxiv.org/abs/1910.01442) goes from 59% to 86% collision-prediction accuracy.
- **Generation:** a new denoiser for [DIAMOND](https://arxiv.org/abs/2405.12399) on Atari Krull cuts FVD by 18.4% and LPIPS by 7.4%, with fewer parameters.

## Citation

```bibtex
@misc{huang2026betterworldmodels,
  title        = {How Much Better Can World Models Get by Changing Only the Architecture?},
  author       = {Huang, Bangzhe and Liu, Ziming},
  year         = {2026},
  month        = nov,
  howpublished = {MetaCircle AI blog},
  url          = {https://metacircleai.github.io/better-world-models/}
}
```

## Repository layout

| Path | Contents |
|:---|:---|
| `content/article.en.md`, `content/article.zh.md` | Source text of the post |
| `index.html`, `zh/index.html` | Generated pages (GitHub Pages serves the repository root) |
| `figures/` | Figures shared by both pages; `figures/m/` holds smaller copies for phones |
| `assets/` | Stylesheet, the [Inter](https://rsms.me/inter/) font and the social-preview image |
| `build.py`, `requirements.txt` | Regenerate both pages: `pip install -r requirements.txt && python build.py` |

## License

Text and figures: [CC BY 4.0](LICENSE). `build.py`: [MIT](LICENSE-CODE). The Inter font is under the SIL Open Font License ([`assets/fonts/LICENSE-Inter.txt`](assets/fonts/LICENSE-Inter.txt)).
