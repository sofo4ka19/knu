package com.parsers;

import com.model.Medicament;
import java.io.File;
import java.util.List;

public interface XmlParser {
    List<Medicament> parse(File file) throws Exception;
}