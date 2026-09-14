"""Legacy curated source retained only for migration and fallback support.

Runtime code should load content through :mod:`data_loader` from ``data/``.
"""

# Technical & Camera Intent Pools (Global)
global_pools = {
    "CAMERA_DEVICE": [
        "iPhone 16 Pro rear camera, native iOS camera pipeline",
        "Sony A7R V mirrorless camera body",
        "Fujifilm X100VI compact digital camera",
        "Canon EOS R5 full-frame mirrorless"
    ],
    "LENS_SPECS": [
        "24mm equivalent wide-angle lens, subtle perspective distortion",
        "35mm f/1.8 handheld street lens, natural eye-level field of view",
        "50mm f/1.4 prime lens, sharp focal plane",
        "85mm f/1.4 portrait lens, creamy smooth background bokeh",
        "135mm f/2.0 candid telephoto lens"
    ],
    "COMPOSITION_FRAMING": [
        "candid waist-up medium portrait framing",
        "tight high-detail upper-body shot",
        "slightly low-angle handheld perspective",
        "eye-level candid composition, rule of thirds",
        "arm's-length high selfie angle"
    ],
    "CAPTURE_INTENT": [
        "friend took the photo candidly from across the table",
        "tripod timer shot, carefully framed but natural posture",
        "phone balanced on a stack of books or shelf, self-timer angle",
        "accidental candid moment, caught mid-movement",
        "professional editorial fashion shoot setup",
        "content creator behind-the-scenes (BTS) capture"
    ],
    "MICRO_EXPRESSION": [
        "subtle, quiet smile with a gentle eye crinkle",
        "soft, relaxed neutral gaze looking directly into the lens",
        "eyes focused downward in deep concentration",
        "looking slightly past the camera, lost in thought",
        "closed-mouth soft grin",
        "biting her lower lip slightly while concentrating",
        "slightly raised eyebrow with a curious, playful expression"
    ],
    "TIME_OF_DAY": [
        "early morning sunrise light",
        "bright midday overhead sun",
        "golden hour late afternoon",
        "blue hour dusk",
        "late night midnight hours"
    ],
    "WEATHER": [
        "crisp clear skies",
        "soft diffused overcast clouds",
        "light misty rain outside",
        "heavy fog filtering soft glow",
        "gentle falling snow visible through windows"
    ],
    "LIGHTING_BEHAVIOR": [
        "soft directional window illumination with subtle shadow falloff",
        "diffused bounce light creating even, natural skin highlights",
        "warm tungsten desk lamp light mixed with cool natural ambient light",
        "soft computer monitor glow reflecting subtly on skin and eyes"
    ],
    "COLOUR_SIMULATION": [
        "natural warm color grading with soft neutrals and clean skin tones",
        "Fujifilm Classic Chrome film simulation with subtle muted greens and deep shadows",
        "clean, high-key modern HDR social media aesthetic",
        "low-contrast editorial color palette with rich dark tones"
    ]
}

LOCKED_CORE_IDENTITY = (
    "East Asian, early 20s, slender build, calm and approachably poised introverted expression, "
    "symmetrical facial features, expressive dark eyes, clear porcelain complexion with natural skin textures. "
    "Wearing her signature delicate silver flower pendant necklace. A tiny, delicate fine-line black ink rose tattoo "
    "is subtly visible behind her right ear, trailing into a thin vertical Japanese proverb down the side of her neck."
)

LOCKED_HAIR_BASE = (
    "dark espresso-brown long hair with subtle natural waves, styled with long, soft, wispy see-through bangs "
    "middle-parted to gently frame her forehead."
)

themes = {
    "1. Home Workstation & SakunaAI Remote Dev": {
        "CASTING": [LOCKED_CORE_IDENTITY],
        "HAIR_STYLING": [
            LOCKED_HAIR_BASE,
            f"{LOCKED_HAIR_BASE} Hair casually pinned up with a minimalist clip, exposing the delicate rose line-art tattoo behind her right ear."
        ],
        "WARDROBE": [
            "signature cream ribbed-knit long-sleeve Henley tee with tiny undone buttons",
            "oversized Tokyo streetwear dark grey hoodie with clean structural lines",
            "cozy off-white heavy cotton waffle-knit sweater"
        ],
        "LOCATION": [
            "her quiet Shibuya residential apartment workspace, bright window light, desk filled with thriving indoor trailing pothos and monsteras, dual coding monitors",
            "minimalist apartment corner desk, mechanical keyboard, small potted botanical plants, and code visible on screens"
        ],
        "PROPS": [
            "wearing custom soft pink over-ear headphones with cute minimalist bunny ear attachments (Sony XMR-54 custom)",
            "holding her signature cherry blossom ceramic coffee mug",
            "custom compact handheld cyberdeck with retro-tech aesthetics resting next to her keyboard"
        ],
        "ACTION": [
            "typing code for SakunaAI with her pink bunny headset on, looking intently at the monitor glow",
            "pausing mid-code to take a sip of coffee, gazing thoughtfully out the window at the quiet Shibuya street",
            "candidly looking up toward the camera with a soft, relaxed gaze, headset resting around her neck"
        ]
    },

    "2. Music Production & Late Night Gaming": {
        "CASTING": [LOCKED_CORE_IDENTITY],
        "HAIR_STYLING": [
            LOCKED_HAIR_BASE,
            f"{LOCKED_HAIR_BASE} Hair casually messy, pulled into a loose bun with wispy side strands."
        ],
        "WARDROBE": [
            "oversized graphic streetwear tee in washed black with minimalist Tokyo typography",
            "fitted charcoal grey ribbed long-sleeve tee paired with comfortable dark lounge pants"
        ],
        "LOCATION": [
            "cozy home studio corner at night, soft ambient LED backlight, audio interface, MIDI keyboard, dual monitors displaying DAW tracks",
            "late-night gaming setup in her Shibuya apartment, soft neon ambient lamp glow"
        ],
        "PROPS": [
            "wearing her iconic pink bunny ear Sony headset, illuminated softly by screen light",
            "adjusting knobs on a compact audio synthesizer unit",
            "holding a frosted glass of iced matcha green tea"
        ],
        "ACTION": [
            "focused on arranging electronic music tracks on her monitor, wearing her bunny ears headset with a subtle smile",
            "leaning back in her ergonomic desk chair, headphones on, eyes closed enjoying a audio playback track",
            "looking down while sketching out graphic design ideas on an iPad tablet"
        ]
    },

    "3. Morning Shibuya Walk & Thrift Bargain Hunting": {
        "CASTING": [LOCKED_CORE_IDENTITY],
        "HAIR_STYLING": [
            LOCKED_HAIR_BASE,
            f"{LOCKED_HAIR_BASE} Tied partially into a sleek half-up half-down style."
        ],
        "WARDROBE": [
            "Tokyo casual minimalist outfit: high-waisted wide-leg tailored trousers, tucked crisp white heavy cotton tee, open light-grey linen overshirt",
            "cropped structured jacket over a beige turtleneck, paired with dark denim and a minimalist crossbody bag",
            "oversized neutral trench coat over a clean monochrome outfit"
        ],
        "LOCATION": [
            "morning Shibuya retail side-street, quiet alleyway with warm natural sunlight and aesthetic local shop facades",
            "charming Shibuya thrift boutique aisle, surrounded by curated vintage clothing racks",
            "outdoor morning market plaza in Shibuya, soft sun filtering through trees"
        ],
        "PROPS": [
            "holding her custom-built mini cyberdeck, using its camera module to take reference photo notes of street art",
            "carrying a minimalist takeaway coffee cup from a local specialty roaster",
            "holding a sleek black tote bag filled with fresh greenery or market finds"
        ],
        "ACTION": [
            "browsing vintage clothing racks, holding a garment up to check the fabric with an engaged look",
            "standing near a sunlit shop window, reviewing photos on her mini cyberdeck screen",
            "walking along a quiet residential Shibuya alley with a coffee in hand, caught in a candid stride"
        ]
    },

    "4. Outdoor Botanical & Apartment Gardening": {
        "CASTING": [LOCKED_CORE_IDENTITY],
        "HAIR_STYLING": [
            LOCKED_HAIR_BASE,
            f"{LOCKED_HAIR_BASE} Loose low ponytail tied with a simple black band."
        ],
        "WARDROBE": [
            "relaxed utility streetwear: beige canvas workwear apron over a simple fitted white long-sleeve tee",
            "loose olive green cargo pants paired with a snug ribbed-knit top"
        ],
        "LOCATION": [
            "sunlit apartment balcony mini-garden, surrounded by lush potted monsteras, trailing ivy, and ceramic planters",
            "indoor apartment garden corner filled with lush green houseplants on tiered wooden plant stands"
        ],
        "PROPS": [
            "holding a vintage brass misting spray bottle",
            "small ceramic plant pot with fresh soil and gardening shears nearby"
        ],
        "ACTION": [
            "gently misting the leaves of a large monstera plant, focusing intently with a peaceful expression",
            "pruning small indoor vines, looking up toward the camera with a gentle, relaxed smile",
            "wiping her forehead with the back of her wrist, mid-task among her green indoor garden"
        ]
    },

    "5. 1999 GTR & Night Drive / Meetup": {
        "CASTING": [LOCKED_CORE_IDENTITY],
        "HAIR_STYLING": [
            LOCKED_HAIR_BASE,
            f"{LOCKED_HAIR_BASE} Hair blowing gently in a soft breeze."
        ],
        "WARDROBE": [
            "techwear-lite aesthetic: high-neck dark olive zip jacket, dark relaxed cargo trousers, clean sneakers",
            "fitted black leather jacket worn casually over a simple off-white scoop neck top"
        ],
        "LOCATION": [
            "standing next to her iconic dark metallic 1999 Nissan Skyline GTR featuring a subtle, elegant cherry blossom side decal, parked under warm city sodium lights",
            "inside the driver seat of her 1999 GTR, dashboard ambient glow reflecting in her eyes, quiet Tokyo urban backdrop"
        ],
        "PROPS": [
            "holding the keys to her 1999 GTR",
            "resting her hand on the steering wheel of the classic GTR",
            "holding her smartphone taking a low-angle photo of her car's cherry blossom decal"
        ],
        "ACTION": [
            "leaning against the hood of her 1999 GTR at night, hands in her jacket pockets with a calm, confident expression",
            "sitting in the driver seat looking out the open window, neon Tokyo city light reflecting off the metallic paint",
            "candidly checking her phone while standing beside her car near a quiet Shibuya street corner"
        ]
    },

    "6. Weekend Socializing & Izakaya / Cafe with Friends": {
        "CASTING": [LOCKED_CORE_IDENTITY],
        "HAIR_STYLING": [
            LOCKED_HAIR_BASE,
            f"{LOCKED_HAIR_BASE} Soft natural waves cascading over shoulders, effortless parted bangs."
        ],
        "WARDROBE": [
            "chic Tokyo night-out style: elegant fine-knit dark sweater with delicate gold huggie earrings",
            "contemporary layered set: dark blazer over a fitted cream inner top, subtle silver chain"
        ],
        "LOCATION": [
            "cozy warm-lit Tokyo izakaya interior, wooden lantern glow, steaming small dishes on the table",
            "trendy Shibuya evening café balcony with warm string lights over background city views"
        ],
        "PROPS": [
            "holding a small glass of iced yuzu soda or craft beverage",
            "her custom mini cyberdeck resting on the wooden dining table next to her phone"
        ],
        "ACTION": [
            "laughing naturally while looking across the table at a friend out of frame, relaxed and out of her introverted shell",
            "candidly smiling mid-conversation while holding her glass",
            "looking back toward the camera with a bright, warm, animated expression"
        ]
    }
}
