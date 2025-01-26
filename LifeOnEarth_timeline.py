import matplotlib.pyplot as plt
import numpy as np

# Define key events in Earth's history (years ago)
events = {
    "Earth forms": 4.6e9,
    "First life (unicellular)": 3.5e9,
    "First eukaryotic cell": 2.1e9,
    "First multicellular organisms": 1.2e9,
    "First vertebrates": 525e6,
    "First land animals": 500e6,
    "First terrestrial plants": 470e6,
    "First reptiles": 310e6,
    "First mammals": 200e6,
    "First birds": 150e6,
    "First flowers": 130e6,
    "First primates": 55e6,
    "First hominids": 6e6,
    "Modern humans": 300e3,
    "  Great Oxidation Event": 2.5e9,
    "  Cambrian explosion": 541e6,
    "  Formation of Pangea": 335e6,
    "  Permian-Triassic extinction event": 252e6,
    "  Cretaceous-Paleogene extinction event": 66e6,
}

# Define categories (Eons and Eras within the Phanerozoic Eon)
categories = {
    "Hadean": (4.6e9, 4.0e9),
    "Archean": (4.0e9, 2.5e9),
    "Proterozoic": (2.5e9, 541e6),
    "Phanerozoic": {
        "Paleozoic": (541e6, 252e6),
        "Mesozoic": (252e6, 66e6),
        "Cenozoic": (66e6, 0),
    },
}

major_events = ["  Great Oxidation Event", "  Cambrian explosion", "  Formation of Pangea", "  Permian-Triassic extinction event", "  Cretaceous-Paleogene extinction event"]

fig, ax = plt.subplots(figsize=(16, 10))  # Increased width for better spacing

# assign vertical positions
event_count = len(events)
y_positions = np.linspace(0, 1, event_count)  # Use normalized vertical positions to fill space

# Plot events on logarithmic scale
for i, (name, time) in enumerate(events.items()):
    y_pos = y_positions[i]
    color = "red" if name in major_events else "blue"
    # Format the time as a power of 10 (e.g., 300e3)
    time_str = f"{time:.0e}".replace('e+0', 'e')  # Remove unnecessary '+0' in scientific notation
    marker = "o" if name in major_events else "D"  # Circles for major events, diamonds for others

    ax.scatter(
        time,
        y_pos,
        color=color,
        marker=marker,
        s=75 if name in major_events else 30,
        label='Major Events' if name in major_events else 'Milestones',
        zorder=5
        )

    ax.text(
        time,
        y_pos - 0.013,
        f"{name} ({time_str})",
        fontsize=9,
        verticalalignment="top",
        horizontalalignment="left",
        color=color
        )

    # Add vertical lines from top to bottom for major events
    if name in major_events:
        ax.vlines(time, ymin=-0.1, ymax=1.1, colors="red", linestyles="dotted", linewidth=2)

# (other) eons
eon_colors = {
    "Hadean": "#A9C6E8",  # Light blue
    "Archean": "#6B9AC4",  # Medium blue
    "Proterozoic": "#3C7D99",  # Dark blue
}

for eon, bounds in categories.items():
    if isinstance(bounds, tuple):  # Eon without subdivisions
        color = eon_colors.get(eon, "lightblue")  # Use assigned color for first three eons
        ax.axvspan(bounds[1], bounds[0], color=color, alpha=0.3, label=eon)
    else:  # Eon with subdivisions (Phanerozoic)
        for era, era_bounds in bounds.items():
            ax.axvspan(
                era_bounds[1],
                era_bounds[0],
                color="lightgreen" if era == "Cenozoic" else "coral" if era == "Mesozoic" else "yellow",
                alpha=0.3,
                label=era
                )

# Remove duplicate labels in legend
handles, labels = ax.get_legend_handles_labels()
unique_labels = dict(zip(labels, handles))
ax.legend(unique_labels.values(), unique_labels.keys(), loc="upper right", fancybox=True, shadow=True)

# Set the x-axis to logarithmic scale
ax.set_xscale("log")

# Set x-axis limits to match the range of events
event_times = list(events.values())
ax.set_xlim(max(event_times) * 1.1, min(event_times) / 1.1)  # Add small buffer around the range

# Adjust y-axis limits to fill the vertical space
ax.set_ylim(-0.05, 1.05)

# Add gridlines for major x-ticks to improve readability
ax.grid(visible=True, which="major", axis="x", linestyle="--", color="gray", alpha=0.7)

# Set x-axis tick parameters to improve readability
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'$10^{{{int(np.log10(x))}}}$'))  # Format ticks as powers of 10
ax.xaxis.minorticks_off()

# Set x-axis ticks to fixed powers of 10 (e.g., 10^3, 10^6, 10^9)
ax.set_xticks([10**i for i in range(int(np.log10(min(event_times))), int(np.log10(max(event_times))) + 1)])

# Add labels and title
ax.set_xlabel("(Logarithmic) Time (years ago)", fontsize=11)
ax.set_title("Evolution of Life on Earth (Logarithmic Scale) — By Evan Maupin | Q4 Bio LK", fontsize=16, weight='medium')
ax.set_ylabel("Normalized vertical space (no function)", fontsize=11)

# Adjust layout for clarity
plt.tight_layout()

# Show the plot
plt.show()
