# WikiLookAlike


## Inspiration

We've been wanting to try face recognition for a while now. What better to try it on than Wikipedia?

## What it does

Finds a Wikipedia page that matches your face as closely as possible

## How I built it

Python, python-face-recognition, pandas, IMDB-WIKI dataset

## Challenges we ran into

We spent several hours calculating face encodings on 3 different computers. This took a lot of our time and and added to the challenge. We also spent a lot of time on data preprocessing. Not all of the data fit our needs so we had to remove some of the data so things would move smoothly.
Accomplishments that I'm proud of

We got a fully functional application made in 24 hours! We had a lot of fun making it and

## What I learned

Data processing, facial recognition

## What's next for WikiLookAlike

Clean up the code a bit. Hopefully optimize it some.


### Citation for IMDB-WIKI dataset. This couldn't have be done without them!
@article{Rothe-IJCV-2018,
  author = {Rasmus Rothe and Radu Timofte and Luc Van Gool},
  title = {Deep expectation of real and apparent age from a single image without facial landmarks},
  journal = {International Journal of Computer Vision},
  volume={126},
  number={2-4},
  pages={144--157},
  year={2018},
  publisher={Springer}
}
