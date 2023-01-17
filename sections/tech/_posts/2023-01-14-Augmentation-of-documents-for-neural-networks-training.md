---
title: Augmentation of documents for neural networks training
published: true
date: 2023-01-14
layout: post
---

## Why augmentation of documents

In training deep learning models it is often useful to perform data augmentation.
Especially when working on documents for OCR training, one may need to have a very large corpus of documents as if they come from real-world offices with folds, gray areas, fax effects or ink-bleeds and scribbles.
Augraphy is a library designed to do that.

This function takes a folder, browse for all the pdf documents contained (you should pass cleaned digital pdf as coming from word or pdf of books) and creates a large number of images.

```
def create_dataset(
    base_pdf_folder: str,
    output_path: str,
    pipeline: AugraphyPipeline,
    shuffle_list:bool=True,
    pages_per_pdf:int=50,
    dpi:int=150
):
    """
    Make sure all the pdf are upright!
    """
    if isinstance(output_path, str):
        output_path = Path(output_path)
        output_path.mkdir(exist_ok=True)
    
    pdf_list = list(Path(base_pdf_folder).rglob("*.pdf"))
    if shuffle_list:
        shuffle(pdf_list) # inplace
    
    N = len(pdf_list)
    pbar = tqdm(pdf_list, total=N)
    for f in pbar:
        pbar.set_postfix_str(f.name)
        try:
            for page_num, page in enumerate(mupdf2image(f, n_pages=pages_per_pdf, dpi=dpi, grayscale=True)):
                augmented = pipeline.augment(np.array(page))["output"]
                pi = Image.fromarray(augmented).convert("L")
                for angle in [0, 180, 90, 270]:
                    output_name = output_path / str(angle) /f.name.replace(".pdf", f"_{page_num}.jpg")
                    pi.rotate(-angle, expand=True, fillcolor=(255,)).save(output_name)
        except Exception as ex:
            print(f"{ex} - {f.name}")
            continue

create_dataset(
    "/Users/carlo/Dropbox/Books/",
    "/Users/carlo/data/textorientation/jpg/aug/",
    pipeline=create_bank_document_pipeline(),
    shuffle_list=True,
    pages_per_pdf=5,
    dpi=150
)
```

Pages are selected at random for every pdf
