package com.parsers;

import com.model.*;
import com.model.Package;

import javax.xml.namespace.QName;
import javax.xml.stream.XMLEventReader;
import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.events.Attribute;
import javax.xml.stream.events.EndElement;
import javax.xml.stream.events.StartElement;
import javax.xml.stream.events.XMLEvent;
import java.io.File;
import java.io.FileInputStream;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class StaxParserImpl implements XmlParser {

    @Override
    public List<Medicament> parse(File file) throws Exception {
        List<Medicament> medicaments = new ArrayList<>();
        XMLInputFactory factory = XMLInputFactory.newInstance();
        XMLEventReader reader = factory.createXMLEventReader(new FileInputStream(file));

        while (reader.hasNext()) {
            XMLEvent event = reader.nextEvent();
            if (event.isStartElement()) {
                StartElement startElement = event.asStartElement();
                if (startElement.getName().getLocalPart().equals("Medicament")) {
                    medicaments.add(parseMedicament(reader, startElement));
                }
            }
        }
        return medicaments;
    }

    private Medicament parseMedicament(XMLEventReader reader, StartElement startElement) throws XMLStreamException {
        Medicament medicament = new Medicament();

        Attribute idAttr = startElement.getAttributeByName(new QName("id"));
        if (idAttr != null) {
            medicament.setId(idAttr.getValue());
        }

        Attribute prescAttr = startElement.getAttributeByName(new QName("prescription"));
        if (prescAttr != null) {
            medicament.setPrescription(Boolean.parseBoolean(prescAttr.getValue()));
        }

        while (reader.hasNext()) {
            XMLEvent event = reader.nextEvent();

            if (event.isStartElement()) {
                StartElement nextStart = event.asStartElement();
                String tagName = nextStart.getName().getLocalPart();

                switch (tagName) {
                    case "Name":
                        medicament.setName(getData(reader));
                        break;
                    case "Pharm":
                        medicament.setPharm(getData(reader));
                        break;
                    case "Group":
                        medicament.setGroup(GroupType.valueOf(getData(reader)));
                        break;
                    case "Analog":
                        medicament.getAnalogs().add(getData(reader));
                        break;
                    case "Version":
                        medicament.getVersions().add(parseVersion(reader));
                        break;
                }
            }
            if (event.isEndElement() &&
                    event.asEndElement().getName().getLocalPart().equals("Medicament")) {
                break;
            }
        }
        return medicament;
    }

    private Version parseVersion(XMLEventReader reader) throws XMLStreamException {
        Version version = new Version();

        while (reader.hasNext()) {
            XMLEvent event = reader.nextEvent();

            if (event.isStartElement()) {
                String tagName = event.asStartElement().getName().getLocalPart();
                switch (tagName) {
                    case "Type":
                        version.setType(getData(reader));
                        break;
                    case "Dosage":
                        version.setDosage(getData(reader));
                        break;
                    case "Certificate":
                        version.setCertificate(parseCertificate(reader));
                        break;
                    case "Package":
                        version.setPack(parsePackage(reader));
                        break;
                }
            }

            if (event.isEndElement() &&
                    event.asEndElement().getName().getLocalPart().equals("Version")) {
                break;
            }
        }
        return version;
    }

    private Certificate parseCertificate(XMLEventReader reader) throws XMLStreamException {
        Certificate cert = new Certificate();
        while (reader.hasNext()) {
            XMLEvent event = reader.nextEvent();
            if (event.isStartElement()) {
                String tagName = event.asStartElement().getName().getLocalPart();
                switch (tagName) {
                    case "Number":
                        cert.setNumber(getData(reader));
                        break;
                    case "IssueDate":
                        cert.setIssueDate(LocalDate.parse(getData(reader)));
                        break;
                    case "ExpirationDate":
                        cert.setExpirationDate(LocalDate.parse(getData(reader)));
                        break;
                    case "RegisteringOrganization":
                        cert.setRegisteringOrganization(getData(reader));
                        break;
                }
            }
            if (event.isEndElement() &&
                    event.asEndElement().getName().getLocalPart().equals("Certificate")) {
                break;
            }
        }
        return cert;
    }

    private Package parsePackage(XMLEventReader reader) throws XMLStreamException {
        Package pack = new Package();
        while (reader.hasNext()) {
            XMLEvent event = reader.nextEvent();
            if (event.isStartElement()) {
                String tagName = event.asStartElement().getName().getLocalPart();
                switch (tagName) {
                    case "Type":
                        pack.setType(getData(reader));
                        break;
                    case "Quantity":
                        pack.setQuantity(Integer.parseInt(getData(reader)));
                        break;
                    case "Price":
                        pack.setPrice(new BigDecimal(getData(reader)));
                        break;
                }
            }
            if (event.isEndElement() &&
                    event.asEndElement().getName().getLocalPart().equals("Package")) {
                break;
            }
        }
        return pack;
    }
    private String getData(XMLEventReader reader) throws XMLStreamException {
        XMLEvent event = reader.nextEvent();
        if (event.isCharacters()) {
            return event.asCharacters().getData();
        }
        return "";
    }
}