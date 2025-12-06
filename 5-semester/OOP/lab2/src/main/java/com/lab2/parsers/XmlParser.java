package com.lab2.parsers;

import com.lab2.model.Medicament;
import java.io.File;
import java.util.List;

public interface XmlParser {
    List<Medicament> parse(File file) throws Exception;
}