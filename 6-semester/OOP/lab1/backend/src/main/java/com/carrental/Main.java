package com.carrental;

import org.apache.catalina.Context;
import org.apache.catalina.connector.Connector;
import org.apache.catalina.startup.Tomcat;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.apache.tomcat.util.descriptor.web.FilterDef;
import org.apache.tomcat.util.descriptor.web.FilterMap;

import java.io.File;

public class Main {

    private static final Logger log = LogManager.getLogger(Main.class);
    private static final int PORT = 8080;

    public static void main(String[] args) throws Exception {
        Tomcat tomcat = new Tomcat();
        tomcat.setPort(PORT);
        tomcat.setBaseDir(System.getProperty("java.io.tmpdir"));

        Context ctx = tomcat.addContext("", new File(".").getAbsolutePath());

        registerServlets(tomcat, ctx);
        registerFilters(ctx);

        tomcat.getConnector();

        tomcat.start();
        log.info("Server started on http://localhost:{}", PORT);
        tomcat.getServer().await();
    }

    private static void registerServlets(Tomcat tomcat, Context ctx) {
        Tomcat.addServlet(ctx, "CarServlet",
                new com.carrental.servlet.CarServlet());
        ctx.addServletMappingDecoded("/api/cars/*", "CarServlet");

        Tomcat.addServlet(ctx, "OrderServlet",
                new com.carrental.servlet.OrderServlet());
        ctx.addServletMappingDecoded("/api/orders/*", "OrderServlet");

        Tomcat.addServlet(ctx, "AdminServlet",
                new com.carrental.servlet.AdminServlet());
        ctx.addServletMappingDecoded("/api/admin/*", "AdminServlet");
    }

    private static void registerFilters(Context ctx) {
        addFilter(ctx, "CorsFilter",
                "com.carrental.filter.CorsFilter", "/*");

        addFilter(ctx, "AuthFilter",
                "com.carrental.filter.AuthFilter", "/api/*");

        addFilter(ctx, "RoleFilter",
                "com.carrental.filter.RoleFilter", "/api/admin/*");
    }

    private static void addFilter(Context ctx, String filterName,
                                  String filterClassName, String urlPattern) {
        FilterDef filterDef = new FilterDef();
        filterDef.setFilterName(filterName);
        filterDef.setFilterClass(filterClassName);
        ctx.addFilterDef(filterDef);

        FilterMap filterMap = new FilterMap();
        filterMap.setFilterName(filterName);
        filterMap.addURLPattern(urlPattern);
        ctx.addFilterMap(filterMap);
    }
}