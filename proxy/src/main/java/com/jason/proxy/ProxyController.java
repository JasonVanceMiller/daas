package com.jason.proxy;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.http.HttpMethod;
import org.springframework.web.bind.annotation.*;

import org.springframework.web.client.RestTemplate;

import jakarta.servlet.http.HttpServletRequest;

import java.util.*;

@RestController
public class ProxyController {

    @Autowired
    private RestTemplate restTemplate;

    @GetMapping("/")
    public ResponseEntity<String> root(HttpServletRequest request) {
        return this.proxy(request, "index.html");
    }

    @GetMapping("/{endpoint}")
    public ResponseEntity<String> proxy(HttpServletRequest request, @PathVariable String endpoint) {
        String uri = "https://raw.githubusercontent.com/JasonVanceMiller/daas/refs/heads/main/frontend/" + endpoint;

        HttpHeaders headers = new HttpHeaders();
        headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));
        headers.add("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36");

        HttpEntity<String> entity = new HttpEntity<>("parameters", headers);
        ResponseEntity<String> result = restTemplate.exchange(uri, HttpMethod.GET, entity, String.class);


        // @HACK total hack. If the media type (MIME) isn't set properly the website won't load.
        if (endpoint.contains(".js")) {
            return ResponseEntity.status(HttpStatus.OK)
                                 .contentType(MediaType.valueOf("application/javascript"))
                                 .body(result.getBody());
        }
        if (endpoint.contains(".html")) {
            return ResponseEntity.status(HttpStatus.OK)
                                 .contentType(MediaType.valueOf("text/html"))
                                 .body(result.getBody());
        }
        if (endpoint.contains(".css")) {
            return ResponseEntity.status(HttpStatus.OK)
                                 .contentType(MediaType.valueOf("text/css"))
                                 .body(result.getBody());
        }
        return ResponseEntity.status(HttpStatus.OK)
                             .contentType(MediaType.TEXT_PLAIN)
                             .body(result.getBody());
    }
}

