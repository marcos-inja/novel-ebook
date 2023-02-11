package org.example;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import nl.siegmann.epublib.domain.Author;
import nl.siegmann.epublib.domain.Book;
import nl.siegmann.epublib.domain.Metadata;
import nl.siegmann.epublib.domain.Resource;
import nl.siegmann.epublib.domain.TOCReference;
import nl.siegmann.epublib.epub.EpubWriter;

public class Main {
  public static void main(String[] args) {
    try {
      Book book = new Book();

      // Set the title
      book.getMetadata().addTitle("Pursuit of the Truth");
      // Add an Author
      book.getMetadata().addAuthor(new Author("Er", "Gen"));

      // Set cover image
      book.setCoverImage(new Resource(Main.class.getResourceAsStream("/chapters/img.png"), "img.png"));
      // Add Chapters
      book.addSection("632", new Resource(Main.class.getResourceAsStream("/chapters/chapter632.html"), "chapter632.html"));
      book.addSection("633", new Resource(Main.class.getResourceAsStream("/chapters/chapter633.html"), "chapter633.html"));
      book.addSection("634", new Resource(Main.class.getResourceAsStream("/chapters/chapter634.html"), "chapter634.html"));

      // Write the Book as Epub
      EpubWriter epubWriter = new EpubWriter();
      epubWriter.write(book, new FileOutputStream("pursuit-of-the-truth.epub"));
    } catch (Exception e) {
      e.printStackTrace();
    }
  }
}