package com.lab2.parsers;

import com.lab2.model.*;
import com.lab2.model.Package;
import com.model.*;
import lab2.model.*;
import org.xml.sax.Attributes;
import org.xml.sax.helpers.DefaultHandler;

import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import java.io.File;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class SaxParserImpl implements XmlParser {

    @Override
    public List<Medicament> parse(File file) throws Exception {
        SAXParserFactory factory = SAXParserFactory.newInstance();
        SAXParser saxParser = factory.newSAXParser();

        MedicamentHandler handler = new MedicamentHandler();
        saxParser.parse(file, handler);

        return handler.getMedicaments();
    }

    private static class MedicamentHandler extends DefaultHandler {
        private List<Medicament> medicaments = new ArrayList<>();
        private Medicament currentMedicament;
        private Version currentVersion;
        private Certificate currentCertificate;
        private Package currentPackage;
        private StringBuilder elementValue;

        public List<Medicament> getMedicaments() {
            return medicaments;
        }

        @Override
        public void startElement(String uri, String localName, String qName, Attributes attributes) {
            elementValue = new StringBuilder();

            switch (qName) {
                case "Medicament":
                    currentMedicament = new Medicament();
                    currentMedicament.setId(attributes.getValue("id"));
                    String prescription = attributes.getValue("prescription");
                    if (prescription != null) {
                        currentMedicament.setPrescription(Boolean.parseBoolean(prescription));
                    }
                    break;
                case "Version":
                    currentVersion = new Version();
                    break;
                case "Certificate":
                    currentCertificate = new Certificate();
                    break;
                case "Package":
                    currentPackage = new Package();
                    break;
            }
        }

        @Override
        public void characters(char[] ch, int start, int length) {
            if (elementValue == null) {
                elementValue = new StringBuilder();
            }
            elementValue.append(ch, start, length);
        }

        @Override
        public void endElement(String uri, String localName, String qName) {
            String value = elementValue.toString().trim();

            switch (qName) {
                // Medicament info
                case "Name":
                    currentMedicament.setName(value);
                    break;
                case "Pharm":
                    currentMedicament.setPharm(value);
                    break;
                case "Group":
                    currentMedicament.setGroup(GroupType.valueOf(value));
                    break;
                case "Analog":
                    currentMedicament.getAnalogs().add(value);
                    break;

                case "Type":
                    if (currentPackage != null) {
                        currentPackage.setType(value);
                    } else if (currentVersion != null) {
                        currentVersion.setType(value);
                    }
                    break;

                // Version info
                case "Dosage":
                    currentVersion.setDosage(value);
                    break;

                // Certificate info
                case "Number":
                    currentCertificate.setNumber(value);
                    break;
                case "IssueDate":
                    currentCertificate.setIssueDate(LocalDate.parse(value));
                    break;
                case "ExpirationDate":
                    currentCertificate.setExpirationDate(LocalDate.parse(value));
                    break;
                case "RegisteringOrganization":
                    currentCertificate.setRegisteringOrganization(value);
                    break;

                // Package info
                case "Quantity":
                    currentPackage.setQuantity(Integer.parseInt(value));
                    break;
                case "Price":
                    currentPackage.setPrice(new BigDecimal(value));
                    break;

                // Closing tags
                case "Package":
                    currentVersion.setPack(currentPackage);
                    currentPackage = null;
                    break;
                case "Certificate":
                    currentVersion.setCertificate(currentCertificate);
                    currentCertificate = null;
                    break;
                case "Version":
                    currentMedicament.getVersions().add(currentVersion);
                    currentVersion = null;
                    break;
                case "Medicament":
                    medicaments.add(currentMedicament);
                    currentMedicament = null;
                    break;
            }
        }
    }
}