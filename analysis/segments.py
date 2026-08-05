"""The defense talk, reconstructed from audience chat alone.

Segments were inferred by Claude (2026-08-04) from a close reading of the
340-message transcript — no slides, recording, or dissertation consulted.
Each segment: time window (minutes since first message), what the chat
suggests was happening on stage, the evidence, and a confidence rating.
"""

SEGMENTS = [
    {
        "start": 0.0,
        "end": 1.5,
        "title": "Doors open: the app reveal",
        "inference": (
            "Near the end of his introduction, Luke unveils xoxowasita.com and "
            "puts the URL on screen. The audience floods in on their phones."
        ),
        "evidence": "20+ greetings in the first 90 seconds; “chat popping off”; “this is like watching a twitch stream”.",
        "confidence": "high",
    },
    {
        "start": 1.5,
        "end": 5.0,
        "title": "Luke's roast-tribute intro: Wasita lore",
        "inference": (
            "The intro's closing stretch, with embarrassing archival photos: Tumblr-teen "
            "era, Brown undergrad, an iconic elevator photo, and a "
            "lonely-kid-to-social-psychologist arc. It lands on the talk's framing: "
            "loneliness is as harmful as smoking (the famous ~15-cigarettes stat, "
            "riffed as “six cigarettes”), and connection can't be captured by "
            "questionnaires — “nobody connects with a survey”."
        ),
        "evidence": "“omg lore drop”; “the iconic elevator pic”; “go brown!!!!!”; “Lonely kid to social psychologist pipeline”; the cigarettes and survey quotes.",
        "confidence": "high",
    },
    {
        "start": 5.0,
        "end": 10.0,
        "title": "Talk begins: why connection, the sad-girl era",
        "inference": (
            "Wasita takes over and motivates the dissertation with her own story of "
            "finding connection online, scored by Phoebe Bridgers. A roadmap of "
            "(at least) three studies goes up — one insider already loves study 3."
        ),
        "evidence": "“Phoebe Bridgers mentioned”; “i too love to be a sad girl”; “Personally I love study 3”; Tumblr full-circle messages from friends who met her there.",
        "confidence": "high",
    },
    {
        "start": 10.0,
        "end": 15.0,
        "title": "Meta interlude: the chat discovers threads",
        "inference": (
            "On stage, likely the transition into methods (a JSTOR link about small "
            "talk suggests a literature beat). In the chat, the audience discovers "
            "reply threads and stress-tests the app while Luke live-comments on "
            "having built it with Claude."
        ),
        "evidence": "A 20-message thread on threads, @mentions, gifs, and Luke's auto-update watchdog; “Please focus on the talk, everyone.”",
        "confidence": "medium",
    },
    {
        "start": 15.0,
        "end": 20.0,
        "title": "Study: shared mental maps of the social world",
        "inference": (
            "A study about mental maps of social relationships — how a group's "
            "shared representation (“vibes”) emerges. The chat immediately "
            "recognizes itself in the construct."
        ),
        "evidence": "“what if the mental map was the vibes we made along the way?”; “just vibes all the way down”; “This chat will be her new final dissertation chapter”.",
        "confidence": "medium",
    },
    {
        "start": 20.0,
        "end": 25.0,
        "title": "She builds it all herself (no AI, no vibes-coding)",
        "inference": (
            "Wasita describes hand-building her experiment platforms — explicitly "
            "without AI assistance — and reads out a Reddit post in which one of "
            "her own study participants wrote about the experiment, signing off "
            "“...and I am not AI”. The chat spirals into jokes about being "
            "training data and an AI Wasita on Zoom."
        ),
        "evidence": "“wasita said no vibe coding happened here”; Luke's {'rawDogging': 'coding without claude'}; “we're being used as training data rn”.",
        "confidence": "high",
    },
    {
        "start": 25.0,
        "end": 29.0,
        "title": "Study: Love Is Blind as naturalistic stimulus",
        "inference": (
            "A study using the reality show Love Is Blind (season-2 cast: Shayne, "
            "Shaina, Natalie) as a naturalistic social stimulus, run on a web app "
            "Wasita built herself — like all her experiment platforms — after "
            "screening many candidate shows."
        ),
        "evidence": "“Shane and Shaina, meant to be”; “they move fast on love is blind”; Luke: “we watched so many shows until we converged on LIB”.",
        "confidence": "high",
    },
    {
        "start": 29.0,
        "end": 34.0,
        "title": "Study with real people: Sush, Clara, the ant — and a donut derail",
        "inference": (
            "A study whose stimuli feature real lab-adjacent people (Sush, Clara, "
            "an Alexis) plus an animated ant character, with beautiful BuPu-palette "
            "figures. Mentions of Mohegan Sun and Krispy Kreme — plausibly "
            "real-world social events used as study material — derail the chat "
            "into a five-minute donut-lore tangent."
        ),
        "evidence": "“Ant is the worst”; “sush and clara will forever haunt the narrative”; “love me some bupu”; the Krispy Kreme campout saga.",
        "confidence": "medium",
    },
    {
        "start": 34.0,
        "end": 40.0,
        "title": "Relatability & synthesis: “WHO CAN RELATE”",
        "inference": (
            "A paradigm about relating to others' experiences (“who can relate”) "
            "closes the empirical arc, then the talk pulls its narrative together."
        ),
        "evidence": "“WHO CAN RELATE”; “i can relate to those who were on tumblr from 2012-2014”; “10/10 storytelling”.",
        "confidence": "medium",
    },
    {
        "start": 40.0,
        "end": 43.0,
        "title": "Talk ends: first applause wave",
        "inference": "The talk proper ends to a wall of congratulations — 30 messages in two minutes.",
        "evidence": "Synchronized “CONGRATS”/“so proud” burst at minute 41–42.",
        "confidence": "high",
    },
    {
        "start": 43.0,
        "end": 63.0,
        "title": "The thank-you slide",
        "inference": (
            "An extended, emotional acknowledgments section: Luke Chang and Thalia "
            "Wheatley (“there's a waitlist” for her cult), Emily Finn's lab, "
            "Eunice, Chris Welker, Amitai's smiling lab, lab Among Us memories, an "
            "unwipeable whiteboard, and personal thanks reaching back to a "
            "formative English teacher, scored by Joji."
        ),
        "evidence": "“I'm not crying. You're crying!”; “Another one joins the Thalia Wheatley cult”; “LOVE Eunice”; “JOJI”; “english teachers are a safe space”.",
        "confidence": "high",
    },
    {
        "start": 63.0,
        "end": 71.0,
        "title": "Final bow: Dr. Mahaphanit",
        "inference": (
            "The defense closes to a second, bigger congratulations wave for "
            "Dr. Mahaphanit."
        ),
        "evidence": "“Congrats Dr. Mahaphanit!!!!!”; second congrats burst at minute 64–66.",
        "confidence": "high",
    },
]

VERDICT = {
    "recoverable": [
        "The talk's narrative arc and section boundaries, almost to the minute",
        "The framing (loneliness/connection, anti-survey, naturalistic methods)",
        "The stimuli (Love Is Blind, reality TV, real friends as characters, an ant)",
        "The personal story (Tumblr, Phoebe Bridgers, English teacher, Joji)",
        "The acknowledgments, nearly name by name",
    ],
    "lost": [
        "That nothing was at stake: this was the public defense — she had "
        "already passed — yet the chat's closing celebration is indistinguishable "
        "from a live verdict moment",
        "Every hypothesis, model, and result — not one effect, statistic, or "
        "conclusion appears in 340 messages",
        "What the studies actually measured or found",
        "Any figure other than its color palette",
    ],
    "punchline": (
        "The chat perfectly preserves the emotional and social contour of the "
        "defense while discarding essentially all of its scientific content — "
        "which is, itself, a finding about what audiences share in real time."
    ),
}
