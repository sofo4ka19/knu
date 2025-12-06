package com.lab2.tool;

import org.xml.sax.SAXException;

import javax.xml.XMLConstants;
import javax.xml.transform.stream.StreamSource;
import javax.xml.validation.Schema;
import javax.xml.validation.SchemaFactory;
import javax.xml.validation.Validator;
import java.io.File;
import java.io.IOException;

public class ValidatorXSD {

    public static boolean isValid(File xmlFile, File xsdFile) {
        if (xmlFile == null || xsdFile == null || !xmlFile.exists() || !xsdFile.exists()) {
            System.err.println("Validation Error: Files do not exist or arguments are null.");
            return false;
        }
        try {
            SchemaFactory factory = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);

            Schema schema = factory.newSchema(xsdFile);

            Validator validator = schema.newValidator();

            validator.validate(new StreamSource(xmlFile));

            System.out.println("Validation is successful: " + xmlFile.getName());
            return true;

        } catch (SAXException e) {
            System.err.println("Validation error: " + e.getMessage());
            return false;
        } catch (IOException e) {
            System.err.println("IO error: " + e.getMessage());
            return false;
        }
    }
}