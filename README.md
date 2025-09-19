Stuff so that I don' forget



Look below for a breakdown of each property.

Colors



Here is a quick breakdown of the color properties:



&nbsp;   --theme-primary - The primary color of the theme. This would be the color used for the button backgrounds.

&nbsp;   --theme-primary-hover - The color you would like the primary color to change to when hovered over.

&nbsp;   --theme-on-primary - The color of text layered on top of the primary color.

&nbsp;   --theme-bg - The background color of the site

&nbsp;   --theme-on-bg - Default body text color

&nbsp;   --theme-surface-1 - The color used for cards layered on top of the background. Think of it like a global accent color or a secondary background color.

&nbsp;   --theme-on-surface-1 - The color used for text on top of the surface-1 color

&nbsp;   --theme-surface-2 - Similar to the surface-1 color but used less often. Feel free to be more creative with this surface to make it pop on the page.

&nbsp;   --theme-on-surface-2 - The color used for text on top of the surface-2 color



Shapes



You’ll notice a lot of rounded corners on the Odyssey Theme but if you look closely when the “Dark” theme is enabled the corners are all hard edges. This is because of the global --theme-shape-radius property. It will determine the shape of things like cards and images.

Transition



Sometimes you want the animations to be consistent, especially on hover effects. This is where you would use the --theme-transition property.

Layouts



&nbsp;   --section-margin - The default top and bottom margin between sections

&nbsp;   --theme-grid-gap - The default gap between items in a grid of cards, images, etc.

&nbsp;   --container-max-width - The default container max width for content

&nbsp;   --container-max-width-narrow - The narrow container max width for content

&nbsp;   --container-padding - The default gutter padding on the container



Custom Font(s)



&nbsp;   Add our own fonts to the /public/assets/fonts directory

&nbsp;   Update the @font-face rules in the src/styles/typography.css file

&nbsp;   Update your font stack with the --theme-font-family-serif and --theme-font-family-sans custom properties.



Adding Your Own Logo



Under src/components/ you’ll see a Logo.astro file that should look something like this:

//<p class="odyssey-logo">Odyssey</p>

//<style>

&nbsp; .odyssey-logo {

&nbsp;   width: fit-content;

&nbsp;   margin: 0;

&nbsp;   font-family: var(--theme-font-family-serif);

&nbsp;   font-size: var(--font-size-md);

&nbsp;   color: inherit;

&nbsp; }

&nbsp; .odyssey-logo:hover {

&nbsp;   text-decoration: underline;

&nbsp;   cursor: pointer;

&nbsp; }

</style>



The easiest way to swap out the Odyssey logo across the site is to replace this code with the SVG code for your company’s logo or using an <img> tag linked to your company logo.

You should see that the Odyssey logo changes across the theme once this is updated.

If you would like more control or don’t like this method of using a <Logo> component you will find most of the components also include a <slot> for the logo which will let you completely replace it.

Favicon

To replace the favicon you simply need to create your own favicon.png file and replace the one found under the public/ folder.

If you don’t want to use a .png file you will need to go to the BaseHead.astro component under src/components/head/ and find this line to replace with your own favicon file.

//<link rel="icon" type="image/png" href="/favicon.png" />

Open Graph / Social Image

To replace the default Open Graph image that displays when the link to your website is shared create your own social.png file and replace the one found under the public/ folder.

