CREATE TABLE wikiquote_pagenames (
    pageid   INT (6),
    pagename TEXT,
    PRIMARY KEY (
        pageid
    )
);

CREATE TABLE wikiquote (
    pageid      INT (6) REFERENCES wikiquote_pagenames (pageid),
    quote_index INT (4),
    quote_text  TEXT,
    PRIMARY KEY (
        pageid,
        quote_index
    )
);
