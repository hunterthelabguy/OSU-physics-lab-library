def meta_text(node):
    return node["c"] if node["t"] == "MetaString" else plain(node["c"])


def span_labels(meta):
    """(first, last) anchors of each span omission's `labels` (D-0189)."""
    out = []
    node = meta.get("ruled_omissions")
    for item in (node["c"] if node and node["t"] == "MetaList" else []):
        span = item["c"].get("span") if item["t"] == "MetaMap" else None
        labels = span["c"].get("labels") if span and span["t"] == "MetaMap" else None
        if labels and labels["t"] == "MetaMap":
            out.append((meta_text(labels["c"]["first"]), meta_text(labels["c"]["last"])))
    return out
