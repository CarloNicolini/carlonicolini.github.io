---
title: Calculate a file hash in Python
layout: post
date: 2023-01-14
---

This code helps you calculating the SHA256 hash of a file in Python. This could be helpful for the disambiguation of different files.

```
def hash_jpg(file: Union[str, Path]) -> str:
    block_size = 65536

    file_hash = hashlib.sha256()
    with open(str(file), 'rb') as fp:
        fb = fp.read(block_size)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = fp.read(block_size)
```

