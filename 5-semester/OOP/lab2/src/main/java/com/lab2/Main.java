package com.lab2;

import com.lab2.model.Version;
import com.lab2.parsers.XmlParser;
import com.lab2.model.Medicament;
import com.lab2.parsers.DomParserImpl;
import com.lab2.parsers.SaxParserImpl;
import com.lab2.parsers.StaxParserImpl;
import com.lab2.tool.MedicamentComparator;
import com.lab2.tool.ValidatorXSD;

import java.io.File;
import java.util.List;

public class Main {

    private static final String XML_PATH = "src/main/resources/Medicine.xml";
    private static final String XSD_PATH = "src/main/resources/Medicine.xsd";

    public static void main(String[] args) {
        File xmlFile = new File(XML_PATH);
        File xsdFile = new File(XSD_PATH);

        System.out.println("\nMEDICINE XML PARSER STARTED\n");

        // 1. Validation
        System.out.println("Validating XML against XSD");
        boolean isValid = ValidatorXSD.isValid(xmlFile, xsdFile);
        if (!isValid) {
            System.err.println("XML is invalid. Execution stopped");
            return;
        }
        System.out.println("Validation successful!\n");

        try {
            // 2. DOM Parser
            runParser(new DomParserImpl(), xmlFile, "DOM");

            // 3. SAX Parser
            runParser(new SaxParserImpl(), xmlFile, "SAX");

            // 4. StAX Parser
            runParser(new StaxParserImpl(), xmlFile, "StAX");

        } catch (Exception e) {
            System.err.println("Critical error during parsing: " + e.getMessage());
            e.printStackTrace();
        }

        System.out.println("ALL OPERATIONS COMPLETED SUCCESSFULLY! ");
    }

    private static void runParser(XmlParser parser, File file, String parserName) throws Exception {
        System.out.println("Parsing using " + parserName + " parser");
        List<Medicament> list = parser.parse(file);

        System.out.println("Parsed " + list.size() + " elements.");
        System.out.println("Sorting data by Group -> Name -> Manufacturer");
        list.sort(MedicamentComparator.BY_GROUP_THEN_NAME_THEN_PHARM);

        System.out.println("\nRESULTS OF (" + parserName + ") PARSER:");
        System.out.println("--------------------------------------------------------------------------------");

        for (Medicament m : list) {
            System.out.printf("[%s] %s%n", m.getId(), m.getName().toUpperCase());
            System.out.printf("  Group: %-15s | Manufacturer: %s%n", m.getGroup(), m.getPharm());

            if (m.getVersions() != null && !m.getVersions().isEmpty()) {
                System.out.println("  Versions:");
                for (Version v : m.getVersions()) {
                    System.out.printf("    - Type: %-10s | Dosage: %s%n", v.getType(), v.getDosage());

                    if (v.getPack() != null) {
                        System.out.printf("      Package: %-8s | Qty: %-3d | Price: %.2f%n",
                                v.getPack().getType(),
                                v.getPack().getQuantity(),
                                v.getPack().getPrice());
                    }
                    if (v.getCertificate() != null) {
                        System.out.printf("      Cert: %-12s (Expires: %s)%n",
                                v.getCertificate().getNumber(),
                                v.getCertificate().getExpirationDate());
                    }
                }
            }
            System.out.println();
        }
    }
}