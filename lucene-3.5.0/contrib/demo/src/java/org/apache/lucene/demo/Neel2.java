package org.apache.lucene.demo;

import java.util.regex.Pattern;

import org.apache.lucene.analysis.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.Term;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.regex.JakartaRegexpCapabilities;
import org.apache.lucene.search.regex.RegexCapabilities;
import org.apache.lucene.search.regex.RegexQuery;
import org.apache.lucene.store.RAMDirectory;

public class Neel2 {
  private static IndexSearcher searcher;
  private static final String FN = "field";

  public static void main(String[] args) throws Exception {
    RAMDirectory directory = new RAMDirectory();
    try {

      IndexWriter writer = new IndexWriter(directory,
            new SimpleAnalyzer(), true,
            IndexWriter.MaxFieldLength.LIMITED);
      Document doc = new Document();
      doc.add(new Field(
                    FN,
                    "hello world",
                    Field.Store.NO, Field.Index.ANALYZED));
      writer.addDocument(doc);
      writer.optimize();
      writer.close();
      searcher = new IndexSearcher(directory, true);

    } catch (Exception e) {
      e.printStackTrace();
    }

    System.err.println(regexQueryNrHits("^hello$", null));

    }

    private static Term newTerm(String value) {
        return new Term(FN, value);
    }

    private static int regexQueryNrHits(String regex, RegexCapabilities capability) throws Exception {

      RegexQuery query = new RegexQuery(newTerm(regex));

      if (capability != null) {
        query.setRegexImplementation(capability);
      }

      return searcher.search(query, null, 1000).totalHits;
    }

}
