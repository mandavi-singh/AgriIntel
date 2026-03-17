# ─── Crop Calendar Data ──────────────────────────────────────
# For each country + crop: sowing, fertilizing, harvesting months

CROP_CALENDAR = {
    "India": {
        "Rice": {
            "Kharif": {
                "sowing":      {"months": "Jun – Jul", "tip": "Sow after first monsoon rains. Transplant seedlings after 25–30 days."},
                "fertilizing": {"months": "Jul – Aug", "tip": "Apply Urea in 3 splits. Top dress at tillering & panicle initiation."},
                "irrigation":  {"months": "Jun – Oct", "tip": "Maintain 2–5 cm standing water. Drain 1 week before harvest."},
                "harvesting":  {"months": "Oct – Nov", "tip": "Harvest when 80% grains turn golden yellow. Use combine harvester."},
            },
            "Rabi": {
                "sowing":      {"months": "Nov – Dec", "tip": "Use short-duration varieties. Pre-soak seeds for 24 hrs."},
                "fertilizing": {"months": "Dec – Jan", "tip": "Basal dose of NPK at sowing. Top dress with Urea at 30 days."},
                "irrigation":  {"months": "Nov – Mar", "tip": "5–6 irrigations needed. Critical stages: tillering, flowering."},
                "harvesting":  {"months": "Mar – Apr", "tip": "Harvest at full maturity. Dry to 14% moisture before storage."},
            },
        },
        "Wheat": {
            "Rabi": {
                "sowing":      {"months": "Oct – Nov", "tip": "Sow in rows 20–22 cm apart. Seed rate 100–125 kg/ha."},
                "fertilizing": {"months": "Nov – Jan", "tip": "NPK basal at sowing. Split Urea at crown root initiation & tillering."},
                "irrigation":  {"months": "Nov – Mar", "tip": "6–8 irrigations. Critical: crown root (21 days), jointing, flowering."},
                "harvesting":  {"months": "Mar – Apr", "tip": "Harvest when leaves dry & grains hard. Avoid delay — shattering risk."},
            },
        },
        "Cotton": {
            "Kharif": {
                "sowing":      {"months": "Apr – Jun", "tip": "Plant after soil temp >18°C. Spacing 60x30 cm for Bt cotton."},
                "fertilizing": {"months": "Jun – Aug", "tip": "High K requirement. Apply at square formation & boll development."},
                "irrigation":  {"months": "Apr – Oct", "tip": "Critical at flowering & boll formation. Avoid water stress."},
                "harvesting":  {"months": "Oct – Jan", "tip": "Pick in 3–4 rounds as bolls open. Early morning picking preferred."},
            },
        },
        "Maize": {
            "Kharif": {
                "sowing":      {"months": "Jun – Jul", "tip": "Sow 2–3 seeds/hill. Thin to 1 after emergence. Depth 3–5 cm."},
                "fertilizing": {"months": "Jul – Aug", "tip": "High N demand. Apply in 3 splits at sowing, knee-high, tasseling."},
                "irrigation":  {"months": "Jun – Sep", "tip": "Critical at knee-high, tasseling, silking, grain fill stages."},
                "harvesting":  {"months": "Sep – Oct", "tip": "Harvest when husks dry & kernels dent. Moisture ~25% at harvest."},
            },
            "Rabi": {
                "sowing":      {"months": "Oct – Nov", "tip": "Use hybrid varieties for winter. Ensure proper drainage."},
                "fertilizing": {"months": "Nov – Dec", "tip": "NPK at planting. Side dress with Urea at 4–6 leaf stage."},
                "irrigation":  {"months": "Nov – Feb", "tip": "4–5 irrigations. Avoid waterlogging in winter."},
                "harvesting":  {"months": "Feb – Mar", "tip": "Harvest at physiological maturity. Dry thoroughly before storage."},
            },
        },
        "Sugarcane": {
            "Annual": {
                "sowing":      {"months": "Oct – Nov (plant cane) / Feb – Mar (ratoon)", "tip": "Use 3-budded setts. Treat with fungicide before planting."},
                "fertilizing": {"months": "Year-round", "tip": "Heavy feeder. Apply N in splits. K important for sugar content."},
                "irrigation":  {"months": "Year-round", "tip": "12–15 irrigations/year. Critical at grand growth phase."},
                "harvesting":  {"months": "Nov – Apr", "tip": "Harvest at 12–14 months. Brix 18–20%. Avoid burning before harvest."},
            },
        },
        "Soybean": {
            "Kharif": {
                "sowing":      {"months": "Jun – Jul", "tip": "Inoculate seeds with Rhizobium. Row spacing 45 cm."},
                "fertilizing": {"months": "Jun – Aug", "tip": "Low N (fixes own). Focus on P and K. Foliar micronutrients help."},
                "irrigation":  {"months": "Jun – Sep", "tip": "Critical at flowering & pod fill. Avoid waterlogging."},
                "harvesting":  {"months": "Sep – Oct", "tip": "Harvest when 95% pods turn brown. Avoid shattering losses."},
            },
        },
        "Barley": {
            "Rabi": {
                "sowing":      {"months": "Oct – Nov", "tip": "Tolerates poor soils. Seed rate 75–100 kg/ha. Shallow sowing."},
                "fertilizing": {"months": "Nov – Dec", "tip": "Moderate N. Excess N reduces malt quality. Apply P at sowing."},
                "irrigation":  {"months": "Nov – Mar", "tip": "2–4 irrigations. Critical at tillering & grain filling."},
                "harvesting":  {"months": "Mar – Apr", "tip": "Harvest early to avoid shattering. Thresh immediately."},
            },
        },
        "Potato": {
            "Rabi": {
                "sowing":      {"months": "Oct – Nov", "tip": "Use certified seed tubers 40–50g. Ridge planting 60x20 cm."},
                "fertilizing": {"months": "Nov – Dec", "tip": "High K for tuber quality. Split N application. Earth up at 30 days."},
                "irrigation":  {"months": "Oct – Feb", "tip": "Frequent light irrigation. Critical at tuber initiation & bulking."},
                "harvesting":  {"months": "Jan – Mar", "tip": "Harvest after haulm senescence. Cure at 15°C for storage."},
            },
        },
        "Tomato": {
            "Kharif": {
                "sowing":      {"months": "Jun – Jul (nursery)", "tip": "Raise nursery first. Transplant at 4–5 leaf stage."},
                "fertilizing": {"months": "Jul – Sep", "tip": "High P for root development. K for fruit quality. Ca prevents BER."},
                "irrigation":  {"months": "Jul – Oct", "tip": "Drip irrigation ideal. Critical at flowering & fruit set."},
                "harvesting":  {"months": "Sep – Nov", "tip": "Pick at breaker stage for markets. Red ripe for processing."},
            },
            "Rabi": {
                "sowing":      {"months": "Sep – Oct (nursery)", "tip": "Transplant in October. Protect from early frost."},
                "fertilizing": {"months": "Oct – Jan", "tip": "Fertigation through drip preferred. Weekly N-K schedule."},
                "irrigation":  {"months": "Oct – Feb", "tip": "Regular irrigation. Mulching reduces water loss."},
                "harvesting":  {"months": "Jan – Mar", "tip": "Main commercial season. Best quality fruits in winter crop."},
            },
        },
        "Carrot": {
            "Rabi": {
                "sowing":      {"months": "Oct – Nov", "tip": "Direct sow in raised beds. Thin to 5–7 cm spacing."},
                "fertilizing": {"months": "Nov – Dec", "tip": "Excess N causes forking. Moderate K for root quality."},
                "irrigation":  {"months": "Oct – Feb", "tip": "Frequent light irrigations. Avoid waterlogging."},
                "harvesting":  {"months": "Jan – Feb", "tip": "Harvest at 90–110 days. Pull by hand or use fork."},
            },
        },
    },
    "USA": {
        "Corn": {
            "Summer": {
                "sowing":      {"months": "Apr – May", "tip": "Plant after last frost. Soil temp >10°C. 30,000–34,000 seeds/acre."},
                "fertilizing": {"months": "May – Jul", "tip": "High N requirement. Side dress at V6 stage. Sulfur often needed."},
                "irrigation":  {"months": "Jun – Aug", "tip": "Critical at VT (tasseling) and R1 (silking). 1 inch/week."},
                "harvesting":  {"months": "Sep – Oct", "tip": "Harvest at 25% moisture for grain. Use combine harvester."},
            },
        },
        "Soybeans": {
            "Summer": {
                "sowing":      {"months": "May – Jun", "tip": "Plant after soil warms to 13°C. Inoculate with Bradyrhizobium."},
                "fertilizing": {"months": "May – Aug", "tip": "Fixes own N. Focus on P, K, S. Tissue test at R3 stage."},
                "irrigation":  {"months": "Jul – Sep", "tip": "Critical at R1–R6. Avoid stress at pod fill."},
                "harvesting":  {"months": "Sep – Oct", "tip": "Harvest at <13% moisture. Check for pod shatter."},
            },
        },
        "Wheat": {
            "Winter": {
                "sowing":      {"months": "Sep – Oct", "tip": "Plant 6 weeks before hard freeze. 1–1.5 inch depth."},
                "fertilizing": {"months": "Oct, Mar – Apr", "tip": "Fall P&K, spring topdress N. Sulfur at green-up."},
                "irrigation":  {"months": "Mar – Jun", "tip": "2–4 irrigations in dryland. Critical at jointing & heading."},
                "harvesting":  {"months": "Jun – Jul", "tip": "Harvest at 13–14% moisture. Watch for weather windows."},
            },
        },
    },
    "Brazil": {
        "Soybeans": {
            "Summer": {
                "sowing":      {"months": "Oct – Dec", "tip": "Plant with onset of rains. Inoculate seeds. 300,000–350,000 plants/ha."},
                "fertilizing": {"months": "Oct – Feb", "tip": "Lime soil to pH 6.2. High P&K demand. Micronutrients important."},
                "irrigation":  {"months": "Oct – Mar", "tip": "Mostly rainfed. Supplement if dry spells exceed 15 days."},
                "harvesting":  {"months": "Feb – Apr", "tip": "Harvest at 13–14% moisture. Fast harvest avoids field losses."},
            },
        },
        "Sugarcane": {
            "Annual": {
                "sowing":      {"months": "Jan – Mar or Aug – Sep", "tip": "Use healthy setts from disease-free fields."},
                "fertilizing": {"months": "Year-round", "tip": "Vinasse application reduces chemical fertilizer need."},
                "irrigation":  {"months": "Jun – Sep (dry season)", "tip": "Rainfed mostly. Irrigate in dry season for ratoon."},
                "harvesting":  {"months": "May – Nov", "tip": "Harvest at 12–14 months. Mechanical harvest common."},
            },
        },
    },
    "Australia": {
        "Wheat": {
            "Winter": {
                "sowing":      {"months": "Apr – Jun", "tip": "Sow after autumn break. Target 150–200 plants/m²."},
                "fertilizing": {"months": "Apr – Aug", "tip": "Starter N&P at sowing. Topdress N at tillering."},
                "irrigation":  {"months": "Mostly rainfed", "tip": "Supplemental irrigation in irrigated zones only."},
                "harvesting":  {"months": "Oct – Dec", "tip": "Harvest at <12% moisture. Watch for summer storms."},
            },
        },
        "Canola": {
            "Winter": {
                "sowing":      {"months": "Apr – May", "tip": "Shallow sowing 1–2 cm. Small seed — fine seedbed essential."},
                "fertilizing": {"months": "Apr – Jul", "tip": "High N&S demand. Boron critical for pod set."},
                "irrigation":  {"months": "Mostly rainfed", "tip": "Drought-sensitive at flowering. Avoid moisture stress."},
                "harvesting":  {"months": "Oct – Nov", "tip": "Swath when 30–40% pods ripe. Harvest at <8% moisture."},
            },
        },
    },
    "China": {
        "Rice": {
            "Summer": {
                "sowing":      {"months": "Apr – May (nursery)", "tip": "Transplant at 3–4 leaf stage. Machine transplanting common."},
                "fertilizing": {"months": "May – Aug", "tip": "Split N in 4 doses. Controlled-release fertilizer used widely."},
                "irrigation":  {"months": "May – Sep", "tip": "Intermittent irrigation saves water. Drain 1 week pre-harvest."},
                "harvesting":  {"months": "Sep – Oct", "tip": "Combine harvester used. Dry quickly to prevent mold."},
            },
        },
        "Wheat": {
            "Winter": {
                "sowing":      {"months": "Oct – Nov", "tip": "Semi-winter varieties dominant. Row spacing 20–25 cm."},
                "fertilizing": {"months": "Oct – Apr", "tip": "Heavy N users. Top dress at green-up & jointing."},
                "irrigation":  {"months": "Nov – May", "tip": "3–4 irrigations. Wintering, jointing, heading stages critical."},
                "harvesting":  {"months": "May – Jun", "tip": "Fast harvest period — mechanized to beat rains."},
            },
        },
    },
}

# ─── For countries not in detail, use generic ────────────────
GENERIC_CALENDAR = {
    "sowing":      {"months": "Varies by region", "tip": "Consult local agricultural extension office for exact dates."},
    "fertilizing": {"months": "At sowing & mid-season", "tip": "Soil test before applying fertilizers for best results."},
    "irrigation":  {"months": "As needed", "tip": "Monitor soil moisture. Irrigate at critical growth stages."},
    "harvesting":  {"months": "After maturity", "tip": "Harvest at right moisture content to minimize losses."},
}

def get_calendar(country, crop):
    country_data = CROP_CALENDAR.get(country, {})
    crop_data    = country_data.get(crop, {})
    if not crop_data:
        return None
    return crop_data

def get_available_crops(country):
    return list(CROP_CALENDAR.get(country, {}).keys())

def get_available_seasons(country, crop):
    country_data = CROP_CALENDAR.get(country, {})
    crop_data    = country_data.get(crop, {})
    return list(crop_data.keys()) if crop_data else []
