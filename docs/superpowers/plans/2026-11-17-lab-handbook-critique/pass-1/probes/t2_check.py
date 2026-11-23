    labels, problems = list(record["labels"]), []
    for first, last in span_labels(doc["meta"]):
        ids = [a for a, _ in labels]
        if first not in ids or last not in ids or ids.index(first) > ids.index(last):
            problems.append(f"span labels {first} to {last}: not a run of Word's labels"
                            " in order (D-0189)")
            continue
        labels = labels[:ids.index(first)] + labels[ids.index(last) + 1:]
    items = rendered_items(md_path)
    return items, problems + compare(labels, items)
