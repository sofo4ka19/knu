package com.parsers;

import com.model.*;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.File;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class DomParserImpl implements XmlParser {

    @Override
    public List<Medicament> parse(File file) throws Exception {
        // Inited DOM builder
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();

        // Parse the file
        Document document = builder.parse(file);
        document.getDocumentElement().normalize();

        List<Medicament> medicaments = new ArrayList<>();

        // Get all list of Medicament
        NodeList nodeList = document.getElementsByTagName("Medicament");

        for (int i = 0; i < nodeList.getLength(); i++) {
            Node node = nodeList.item(i);
            if (node.getNodeType() == Node.ELEMENT_NODE) {
                Element element = (Element) node;

                medicaments.add(parseMedicament(element));
            }
        }
        return medicaments;
    }

    private String getElementTextContent(Element parent, String tagName) {
        NodeList nodeList = parent.getElementsByTagName(tagName);
        if (nodeList.getLength() > 0) {
            return nodeList.item(0).getTextContent();
        }
        return null;
    }

    private Medicament parseMedicament(Element element) {
        return new Medicament();
    }
}