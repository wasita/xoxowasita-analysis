"""The defense talk, minute by minute — verified against the Zoom recording.

Segments were first inferred from the audience chat alone, then corrected
against the recording's transcript (data/local/, not committed). Times are
minutes on the chat clock (0 = first chat message); the recording starts
17 minutes earlier, mid-way through Luke's introduction.
"""

SEGMENTS = [
    {
        "start": 0.0,
        "end": 2.0,
        "title": "She begins: how do we connect?",
        "inference": (
            "Luke caps his introduction by unveiling xoxowasita.com — built from "
            "the Slack message Wasita sent him 14 months earlier asking for "
            "exactly this. She takes the stage with her PhD question: how do two "
            "strangers become people who feel close? Her honest why: for a long "
            "time she didn't know how to make friends — until Tumblr, and the "
            "13-person STEM pre-orientation crew of her freshman year."
        ),
        "evidence": "The chat floods in with 20+ hellos in 90 seconds; “omg lore drop”; “go brown!!!!!”.",
        "confidence": "verified",
    },
    {
        "start": 2.0,
        "end": 4.5,
        "title": "The stakes, and the three routes",
        "inference": (
            "The Surgeon General calls loneliness an epidemic — as dangerous as "
            "15 cigarettes a day. But she inverts the question: not what happens "
            "when connection fails, how it works when it succeeds. The literature's "
            "three routes — commonalities, good conversation, shared experience — "
            "are real but tangled together, and mostly studied in artificial ways."
        ),
        "evidence": "“this talk is just a secret ad planted by big tobacco”; Ben budgeting his six cigarettes a day.",
        "confidence": "verified",
    },
    {
        "start": 4.5,
        "end": 6.5,
        "title": "Control vs naturalism: choose both",
        "inference": (
            "The methodological stance: questionnaires buy control but “nobody "
            "actually connects with a survey”; observation buys real life but no "
            "causality. Her answer — custom multi-user platforms she builds "
            "herself, where real people talk freely while something hidden in the "
            "interaction is quietly manipulated."
        ),
        "evidence": "“nobody connects with a survey” quoted straight into the chat.",
        "confidence": "verified",
    },
    {
        "start": 6.5,
        "end": 8.0,
        "title": "One process: inferring minds through conversation",
        "inference": (
            "The framework: connection is the feeling you get when inference says "
            "this person sees the world the way I do. Three studies probe it — "
            "what one learned belief does to your model of a whole person, what a "
            "partner's reaction timing reveals, and how deeply something must be "
            "shared to count."
        ),
        "evidence": "“Personally I love study 3” — Jonathan Phillips, committee member, no spoilers given.",
        "confidence": "verified",
    },
    {
        "start": 8.0,
        "end": 12.0,
        "title": "Study 1: one stance at a wedding",
        "inference": (
            "Wedding small talk as foraging for common ground. Her real example: "
            "an early conversation with her friend and co-author Chris landed on "
            "Phoebe Bridgers, and she walked away inferring a whole shared "
            "worldview. The study: strangers state beliefs on 35 topics, chat for "
            "three minutes about exactly one, then guess the other 34 — against a "
            "control group shown the answer with no conversation. (Meanwhile the "
            "chat discovers reply threads and stress-tests Luke's app.)"
        ),
        "evidence": "“Phoebe Bridgers mentioned”; Katie!'s JSTOR small-talk link; the 20-message thread about threads; “Please focus on the talk, everyone.”",
        "confidence": "verified",
    },
    {
        "start": 12.0,
        "end": 17.0,
        "title": "Study 1 results: the mental map",
        "inference": (
            "One agreement propagates to related topics and fades with distance; "
            "one disagreement doesn't close the door. Conversation raises the "
            "floor most for the worst first impressions. Computational model "
            "comparison: people aren't projecting themselves onto others — they "
            "navigate a shared population map of how beliefs hang together."
        ),
        "evidence": "“But what if the mental map was the vibes we made along the way?”; “Its just vibes all the way down”.",
        "confidence": "verified",
    },
    {
        "start": 17.0,
        "end": 20.0,
        "title": "Study 2 origin: pandemic Slack with Alexis & Clara",
        "inference": (
            "Nobody had studied people talking through a shared experience as it "
            "happens (closest attempt: strangers eating chocolate in silence). Her "
            "grad school started on Zoom — so she, Alexis, and Clara lived on "
            "Slack, reacting together to everything in real time. She rebuilt "
            "exactly that in the lab."
        ),
        "evidence": "“This chat will be her new final dissertation chapter”; “in 2026 we get zoom + xoxowasita”; the room realizes it is the paradigm.",
        "confidence": "verified",
    },
    {
        "start": 20.0,
        "end": 24.0,
        "title": "Study 2: Love Is Blind, no LLMs, real connection",
        "inference": (
            "Pre-LLM, so she was “just raw dogging it”: a custom co-watching app "
            "where four strangers watch 30 minutes of Love Is Blind and chat. They "
            "reach connection levels other work finds between actual friends. "
            "Reply patterns and word echoes predict who feels close to whom."
        ),
        "evidence": "Luke's {'rawDogging': 'coding without claude'}; “wasita said no vibe coding happened here”; “Natural intelligence ftw”.",
        "confidence": "verified",
    },
    {
        "start": 24.0,
        "end": 30.0,
        "title": "The secret split",
        "inference": (
            "The hidden manipulation: mid-show the stream silently forks — two "
            "viewers follow Shane's story with Natalie, two with Shaina; same "
            "beginning, same ending. Nobody noticed. Scoring each chat message "
            "against the show's meaning, moment by moment: a partner whose words "
            "track your moment feels closer — and the effect switches on exactly "
            "when the screens diverge and off when they rejoin."
        ),
        "evidence": "“Shane and Shaina, meant to be”; “what are the odds we are watching 2 different versions of this dissertation right now?” — closer to the truth than the chat knew.",
        "confidence": "verified",
    },
    {
        "start": 30.0,
        "end": 32.0,
        "title": "Blaming minds, not screens",
        "inference": (
            "Since nobody suspects the screens differ, a partner reacting to the "
            "wrong moments can only mean one thing: they're of a different mind. "
            "Flip it, and a well-timed reaction becomes a window into a shared "
            "one — which is what those pandemic Slack threads were all along."
        ),
        "evidence": "“wow throwback to among us”; “who was the imposter”; “SUSSSSS”.",
        "confidence": "verified",
    },
    {
        "start": 32.0,
        "end": 38.0,
        "title": "Study 3: Mohegan Sun, Krispy Kreme, and Sush",
        "inference": (
            "Her childhood weekends at a casino arcade got blank stares — until "
            "Sush said I can relate. The study: a disclosure game separating "
            "having heard of, having lived, and relating. Relating towers over the "
            "rest — and relating to something rare counts far more than relating "
            "to Easy Mac, because rare commonalities are diagnostic: hers and "
            "Sush's pointed straight to first-generation immigrant childhoods."
        ),
        "evidence": "The five-minute Krispy Kreme derail; “WHO CAN RELATE”; “never suspicious of sushpicious”.",
        "confidence": "verified",
    },
    {
        "start": 38.0,
        "end": 41.5,
        "title": "Synthesis: as connecting as it is revealing",
        "inference": (
            "Three studies, one process: we're always inferring who someone is "
            "through conversation, and connection is what it feels like when the "
            "inference says they see the world your way. Her two friendships prove "
            "the frame from opposite ends — internet friends who shared nothing "
            "but words, a college crew who shared everything — same result. “Every "
            "so often, someone pays attention, and something special happens.”"
        ),
        "evidence": "“we love a narrative”; “10/10 storytelling”; the first applause wall at minute 41.",
        "confidence": "verified",
    },
    {
        "start": 41.5,
        "end": 63.0,
        "title": "The thank you slides",
        "inference": (
            "Twenty minutes of acknowledgments: her committee — Robert Hawkins, "
            "Jonathan Phillips, Thalia Wheatley — plus Luke's own slide, Eunice, "
            "and Eshin, who flew in from San Diego and whose talk made her want "
            "to build interactive experiments in the first place. The lab and the "
            "Asian girl gang, Grace, Sush, Alexis (“my favorite person to share "
            "reality with”), the Frank Lab and Romy, her partner Noah, Joji the "
            "cat, OG Tumblr friend Jackie Chang, her English teacher Lori, her "
            "cousin, and her parents — “both of my Ivy League degrees are yours”."
        ),
        "evidence": "“I'm not crying. You're crying!”; “Another one joins the Thalia Wheatley cult”; “LOVE Eunice”; “JOJI”.",
        "confidence": "verified",
    },
    {
        "start": 63.0,
        "end": 66.0,
        "title": "Severely over time, out of love",
        "inference": (
            "“Okay, we're severely over time, it's 4:20” — a rooftop reception is "
            "announced, and the chat delivers its final congratulations wave for "
            "Dr. Mahaphanit."
        ),
        "evidence": "“Congrats Dr. Mahaphanit!!!!!”; the second congrats burst at minutes 64–66.",
        "confidence": "verified",
    },
]

VERDICT = {
    "recoverable": [
        "The narrative arc and section boundaries, almost to the minute",
        "The framing (loneliness/connection, anti-survey, naturalism + control)",
        "The stimuli and stories (Love Is Blind, Phoebe Bridgers, Krispy Kreme, Sush)",
        "The personal history (Tumblr, Brown, the English teacher)",
        "The acknowledgments, nearly name by name",
    ],
    "lost": [
        "Every result: the propagation curves, the mental-map model win, the "
        "connection boost that switches on with the split, the rarity premium — "
        "none of it surfaced in 340 messages",
        "The secret stream split itself — the chat joked about “watching 2 "
        "different versions” without knowing that was literally the manipulation",
        "That nothing was at stake: this was the public defense — she had already "
        "passed — yet the closing celebration is indistinguishable from a live "
        "verdict moment",
    ],
    "punchline": (
        "The chat perfectly preserves the emotional and social contour of the "
        "defense while discarding essentially all of its scientific content — "
        "which is, itself, a finding about what audiences share in real time."
    ),
}
