# JainNav 🧭

**Campus navigation, made simpler.**

[**Try JainNav**](https://harshashetty6233-dot.github.io/JainNav/) · [**View the campus floor sketches**](docs/floors-sketch.pdf)

JainNav is a campus navigation project that helps visitors find a route between a starting room/location and a destination. The interface includes an **Avoid Stairs** option for routes where stair-free travel is preferred.

> **Community project:** Campus layouts, room numbers and access routes can change. This repository welcomes corrections and improvements from people familiar with the building.

## 🗺️ Campus floor sketches

The [five-page floor sketch PDF](docs/floors-sketch.pdf) is a reference for understanding the building layout and proposing updates.

| Sketch page | Level shown | Examples of details |
| --- | --- | --- |
| 1 | Ground level | Amphitheatre, numbered rooms, corridor and staircase entries |
| 2 | First floor | Rooms in the 100 series, first-floor hall and corridor |
| 3 | Second floor | Rooms in the 200 series, library and library corridor |
| 4 | Third floor | Rooms in the 300 series, library seating hall |
| 5 | Fourth floor | Rooms in the 400 series, fourth-floor hall and corridor |

The legend distinguishes **staircase entries**, **hatched fault spaces**, **rooms**, and **corridors**. Staircase labels (such as `SA`, `SB`, `SC`, `SD`, `SP`, `SQ`, `SX` and `SY`) appear across the sketches; consult the individual page for their positions.

**Note:** These are reference sketches, not a certified architectural plan or an accessibility audit. Verify any route and room-location change on site before merging it.

## 🚀 How to use JainNav

1. Open the [live website](https://harshashetty6233-dot.github.io/JainNav/).
2. Enter the **Starting Point** room/location ID.
3. Enter the **Destination** room/location ID.
4. Enable **Avoid Stairs** if needed.
5. Press **BASH** to request a route.

The interface is built with web technologies and published as a static website using GitHub Pages. The exact route calculation and data representation should be checked in the source code before changing the navigation logic.

## 🧰 Technologies

- **HTML** — page structure
- **JavaScript** — browser-side interaction
- **Python** — used in the project workflow (see the repository for its specific role)
- **GitHub Pages** — deployment of the static site

## 🤝 Contributing

**New to GitHub?** You can help even if you only notice an incorrect room label or staircase location.

### Suggest a correction

1. Check the [floor sketches](docs/floors-sketch.pdf) and the [live website](https://harshashetty6233-dot.github.io/JainNav/).
2. Open the repository's **Issues** tab and create an issue (if issues are enabled).
3. Describe the **floor**, **room/staircase ID**, **what is wrong**, and **what should change**. Attach a photo or annotated sketch only if you have permission to share it.

### Submit a code or map change

1. **Fork** this repository on GitHub.
2. Create a branch, for example `fix/second-floor-room-label`.
3. Update the relevant map data, HTML, JavaScript or documentation. If the reference sketch itself changes, replace `docs/floors-sketch.pdf` with a revised PDF.
4. Test the affected routes, including **Avoid Stairs** when relevant.
5. Commit your changes with a clear message, such as `Fix second-floor room label`.
6. Open a **Pull Request** to this repository. Explain what changed, why, and how you verified it.

### Useful information to include in a PR

- Floor and affected room/staircase IDs
- Before/after description or screenshots
- Whether normal routing and **Avoid Stairs** were tested
- Any uncertainty that needs on-campus verification

Please avoid publishing personal information, restricted areas or sensitive access details.

## 📄 Floor-plan source

The sketches are provided as a contribution reference. **Do not assume they are free to reuse outside this project**; confirm you have permission to publish and redistribute them before uploading.

---

Built to make campus navigation easier. Contributions and corrections are welcome!
