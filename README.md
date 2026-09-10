# Nassau Candy – Factory-to-Customer Shipping Route Efficiency Analysis

Interactive data analytics project analyzing shipping routes, lead times, factories, regions, geographic bottlenecks and ship modes for Nassau Candy Distributor.

## Tech Stack
Python • Pandas • Plotly • Streamlit

## Dashboard
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project Highlights
- 10,194 shipment records
- 196 factory-to-destination routes
- Factory, region and ship-mode comparisons
- Route efficiency scoring
- Geographic bottleneck identification
- Interactive filters and route drill-down
- Order-level lead-time timeline

## Key Findings
- Lot's O' Nuts is the largest factory by shipment volume.
- Wicked Choccy's is the second-largest factory by shipment volume.
- Several routes show very low lead times while others are major bottlenecks.
- Standard Class has the highest shipment volume.
- Tennessee, Indiana and Washington are examples of higher-volume geographic bottlenecks.

## Data Validation Note
The supplied source dates produce unusually large lead-time values (roughly 904–1642 days). The project retains these values for analysis consistency; the source dates should be validated before operational use.
