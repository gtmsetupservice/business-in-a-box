---
layout: default
title: Blog - LocallyKnown.pro
description: WordPress development insights, technical case studies, and website optimization tips for local businesses.
---

# Blog

<div id="blog" class="max-w-4xl mx-auto px-4 py-12 text-center">
    <header class="text-center mb-12">
        <h1 class="text-4xl font-bold mb-4">WordPress Development Insights</h1>
        <p class="text-xl text-gray-600">Technical case studies, troubleshooting guides, and optimization tips for local business websites</p>
    </header>

    <!-- Blog Posts Grid -->
    <div class="grid md:grid-cols-1 lg:grid-cols-2 gap-8 max-w-4xl mx-auto">
        {% for post in site.posts %}
        <article class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
            <!-- Featured Image (if available) -->
            {% if post.image %}
            <div class="h-48 bg-gray-200 overflow-hidden">
                <img src="{{ post.image }}" alt="{{ post.title }}" class="w-full h-full object-cover">
            </div>
            {% else %}
            <div class="h-48 bg-gradient-to-r from-blue-500 to-blue-600 flex items-center justify-center">
                <span class="text-white text-2xl font-bold">{{ post.title | truncate: 3, "" | upcase }}</span>
            </div>
            {% endif %}

            <div class="p-6">
                <!-- Categories -->
                {% if post.categories %}
                <div class="mb-3">
                    {% for category in post.categories %}
                    <span class="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded mr-2">{{ category }}</span>
                    {% endfor %}
                </div>
                {% endif %}

                <!-- Title -->
                <h2 class="text-xl font-bold mb-3 line-clamp-2">
                    <a href="{{ post.url }}" class="text-gray-900 hover:text-blue-600 transition-colors">{{ post.title }}</a>
                </h2>

                <!-- Description -->
                {% if post.description %}
                <p class="text-gray-600 mb-4 line-clamp-3">{{ post.description }}</p>
                {% else %}
                <p class="text-gray-600 mb-4 line-clamp-3">{{ post.excerpt | strip_html | truncate: 150 }}</p>
                {% endif %}

                <!-- Meta Info -->
                <div class="flex items-center text-sm text-gray-500 mb-4">
                    <time datetime="{{ post.date | date_to_xmlschema }}">
                        {{ post.date | date: "%B %d, %Y" }}
                    </time>

                    <!-- Reading Time -->
                    {% assign words = post.content | strip_html | number_of_words %}
                    {% assign reading_time = words | divided_by: 200 | at_least: 1 %}
                    <span class="mx-2">•</span>
                    <span>{{ reading_time }} min read</span>
                </div>

                <!-- Read More Button -->
                <a href="{{ post.url }}" class="inline-block bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition-colors">
                    Read More →
                </a>
            </div>
        </article>
        {% endfor %}
    </div>

    <!-- No Posts Message -->
    {% if site.posts.size == 0 %}
    <div class="text-center py-12">
        <h2 class="text-2xl font-bold text-gray-600 mb-4">No posts yet</h2>
        <p class="text-gray-500">Check back soon for WordPress development insights and case studies!</p>
    </div>
    {% endif %}

    <!-- Newsletter Signup -->
    <div class="mt-16 bg-gradient-to-r from-orange-600 to-red-600 text-white rounded-lg p-8 text-center">
        <h3 class="text-2xl font-bold mb-4">Stay Updated</h3>
        <p class="text-lg mb-6">Get the latest WordPress development tips and case studies delivered to your inbox.</p>
        <div class="max-w-md mx-auto">
            <form class="flex gap-3">
                <input type="email" placeholder="Enter your email" class="flex-1 px-4 py-2 rounded text-gray-900">
                <button type="submit" class="bg-green-500 hover:bg-green-600 px-6 py-2 rounded font-bold transition-colors">
                    Subscribe
                </button>
            </form>
        </div>
    </div>
</div>

<style>
/* Line clamp utility classes */
.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>