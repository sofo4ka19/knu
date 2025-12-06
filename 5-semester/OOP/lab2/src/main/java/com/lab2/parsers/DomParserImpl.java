package com.lab2.parsers;

import com.lab2.model.Package;
import com.lab2.model.Certificate;
import com.lab2.model.GroupType;
import com.lab2.model.Medicament;
import com.lab2.model.Version;
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
        Medicament medicament = new Medicament();

        medicament.setId(element.getAttribute("id"));
        if (element.hasAttribute("prescription")) {
            medicament.setPrescription(Boolean.parseBoolean(element.getAttribute("prescription")));
        }

        medicament.setName(getElementTextContent(element, "Name"));
        medicament.setPharm(getElementTextContent(element, "Pharm"));

        String groupStr = getElementTextContent(element, "Group");
        medicament.setGroup(GroupType.valueOf(groupStr));

        NodeList analogsNode = element.getElementsByTagName("Analog");
        List<String> analogsList = new ArrayList<>();
        for (int i = 0; i < analogsNode.getLength(); i++) {
            analogsList.add(analogsNode.item(i).getTextContent());
        }
        medicament.setAnalogs(analogsList);

        medicament.setVersions(parseVersions(element));

        return medicament;
    }

    private List<Version> parseVersions(Element parentElement) {
        List<Version> versions = new ArrayList<>();
        NodeList versionsNodes = parentElement.getElementsByTagName("Version");

        for (int i = 0; i < versionsNodes.getLength(); i++) {
            Node node = versionsNodes.item(i);
            if (node.getNodeType() == Node.ELEMENT_NODE) {
                Element versionElement = (Element) node;
                Version version = new Version();

                version.setType(getElementTextContent(versionElement, "Type"));
                version.setDosage(getElementTextContent(versionElement, "Dosage"));
                version.setCertificate(parseCertificate(versionElement));
                version.setPack(parsePackage(versionElement));

                versions.add(version);
            }
        }
        return versions;
    }

    private Certificate parseCertificate(Element versionElement) {
        Certificate cert = new Certificate();
        Element certElement = (Element) versionElement.getElementsByTagName("Certificate").item(0);

        cert.setNumber(getElementTextContent(certElement, "Number"));
        cert.setRegisteringOrganization(getElementTextContent(certElement, "RegisteringOrganization"));

        cert.setIssueDate(LocalDate.parse(getElementTextContent(certElement, "IssueDate")));
        cert.setExpirationDate(LocalDate.parse(getElementTextContent(certElement, "ExpirationDate")));

        return cert;
    }

    private Package parsePackage(Element versionElement) {
        Package pack = new Package();
        Element packElement = (Element) versionElement.getElementsByTagName("Package").item(0);

        pack.setType(getElementTextContent(packElement, "Type"));

        String qty = getElementTextContent(packElement, "Quantity");
        pack.setQuantity(Integer.parseInt(qty));

        String price = getElementTextContent(packElement, "Price");
        pack.setPrice(new BigDecimal(price));

        return pack;
    }
}