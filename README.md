# Stain normalization.

Implementation of a few common stain normalization techniques ([Reinhard](http://ieeexplore.ieee.org/document/946629/), [Macenko](http://ieeexplore.ieee.org/document/5193250/), [Vahadane](http://ieeexplore.ieee.org/document/7164042/)) in Python. 

For usage see the notebook ```demo.ipynb```

In short do something like

```
n = stainNorm_Reinhard.normalizer()
n.fit(target_image)
out=n.transform(source_image)
```

If you want Hematoxylin do something like

```
n = stainNorm_Vahadane.normalizer()
out = n.hematoxylin(source_image)
```

Here we show the application of the techniques to a few images (in data folder). We normalize to the first image and for Macenko and Vahadane also show the extracted Hematoxylin channel.

Below that are a few more challenging images (also in data folder).

The images are taken from the [ICIAR 2018 challenge](https://iciar2018-challenge.grand-challenge.org/).

One change to the vanilla methods is used. With all images we first apply a brightness standardizing step (below). This is especially useful in handling the more challenging images (which are typically too dim) and does not damage performance for the other images. 

```
def standardize_brightness(I):
    """

    :param I:
    :return:
    """
    p = np.percentile(I, 90)
    return np.clip(I * 255.0 / p, 0, 255).astype(np.uint8)
```

## Original images

<a href="https://imgur.com/Il63NLV"><img src="https://i.imgur.com/Il63NLV.png" title="source: imgur.com" /></a>

## Reinhard

*E. Reinhard, M. Adhikhmin, B. Gooch, and P. Shirley, ‘Color transfer between images’, IEEE Computer Graphics and Applications, vol. 21, no. 5, pp. 34–41, Sep. 2001.*


<a href="https://imgur.com/eknRYiN"><img src="https://i.imgur.com/eknRYiN.png" title="source: imgur.com" /></a>

## Macenko

*M. Macenko et al., ‘A method for normalizing histology slides for quantitative analysis’, in 2009 IEEE International Symposium on Biomedical Imaging: From Nano to Macro, 2009, pp. 1107–1110.*

<a href="https://imgur.com/WadPHuc"><img src="https://i.imgur.com/WadPHuc.png" title="source: imgur.com" /></a>

<a href="https://imgur.com/0FyOEVG"><img src="https://i.imgur.com/0FyOEVG.png" title="source: imgur.com" /></a>

## Vahadane

*A. Vahadane et al., ‘Structure-Preserving Color Normalization and Sparse Stain Separation for Histological Images’, IEEE Transactions on Medical Imaging, vol. 35, no. 8, pp. 1962–1971, Aug. 2016.*

<a href="https://imgur.com/61dnNCE"><img src="https://i.imgur.com/61dnNCE.png" title="source: imgur.com" /></a>

<a href="https://imgur.com/0FyOEVG"><img src="https://i.imgur.com/0FyOEVG.png" title="source: imgur.com" /></a>

# More challenging images

## Original images

<a href="https://imgur.com/rovxJsL"><img src="https://i.imgur.com/rovxJsL.png" title="source: imgur.com" /></a>

## Reinhard

<a href="https://imgur.com/leVjKEt"><img src="https://i.imgur.com/leVjKEt.png" title="source: imgur.com" /></a>

## Macenko

<a href="https://imgur.com/vhTGR0R"><img src="https://i.imgur.com/vhTGR0R.png" title="source: imgur.com" /></a>

## Vahadane

<a href="https://imgur.com/0j9SWF8"><img src="https://i.imgur.com/0j9SWF8.png" title="source: imgur.com" /></a>