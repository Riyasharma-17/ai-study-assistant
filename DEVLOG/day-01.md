# AI Study Assistant — Day 1

## Goal
Extract text from a PDF.

## What I built
Created a `read_pdf(path)` function in `pdf_reader.py` that reads a PDF and returns extracted text.

## How it works
Used `PyPDF2.PdfReader` to open the file, looped through all pages, extracted text from each page, and combined it into one string.

## What I learned
- External library usage
- File handling
- Functions with a single responsibility
- Basic OOP object usage

## Result
The program successfully reads a PDF and prints extracted text in the terminal.