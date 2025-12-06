package com.lab2;

import com.lab2.model.Medicament;
import com.lab2.parsers.DomParserImpl;
import com.lab2.parsers.SaxParserImpl;
import com.lab2.parsers.StaxParserImpl;
import com.lab2.parsers.XmlParser;
import org.junit.jupiter.api.Test;
import java.io.File;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

class XmlParsersTest {

    private final File xmlFile = new File("src/main/resources/Medicine.xml");

    @Test
    void testDomParser() throws Exception {
        runParserTest(new DomParserImpl());
    }

    @Test
    void testSaxParser() throws Exception {
        runParserTest(new SaxParserImpl());
    }

    @Test
    void testStaxParser() throws Exception {
        runParserTest(new StaxParserImpl());
    }

    @Test
    void testDateParsingCorrectness() throws Exception {
        Medicament m = new DomParserImpl().parse(new File("src/main/resources/Medicine.xml")).get(0);
        java.time.LocalDate issueDate = m.getVersions().get(0).getCertificate().getIssueDate();

        assertEquals(2023, issueDate.getYear());
        assertEquals(1, issueDate.getMonthValue());
        assertEquals(15, issueDate.getDayOfMonth());
    }

    private void runParserTest(XmlParser parser) throws Exception {
        assertTrue(xmlFile.exists(), "Test XML file not found!");

        List<Medicament> list = parser.parse(xmlFile);

        assertNotNull(list);
        assertEquals(6, list.size(), "Should parse exactly 6 medicaments");

        Medicament first = list.get(0);

        assertEquals("med01", first.getId());
        assertEquals("Amoxicillin", first.getName());
        assertTrue(first.isPrescription());

        assertNotNull(first.getVersions());
        assertFalse(first.getVersions().isEmpty());
        assertEquals("Tablets", first.getVersions().get(0).getType());
    }
}