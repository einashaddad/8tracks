8tracks
=======

This is an implementation of PageRank and a web scraper for 8tracks.com; ran on approximately 100,000 users and 200,000 connections to find the best people to follow.

* eight_tracks.py : Scrapes 8tracks starting at a seed user and outputs the graph used by the PageRank algorithm to a file.
* page_rank.py : Returns the top 10 users to follow on 8tracks

To run with specified genre:
    python page_rank.py electronic

To run on entire graph:
    python page_rank.py
    
