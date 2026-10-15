import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np

def create_system_architecture():
    fig, ax = plt.subplots(figsize=(15.5, 7.2), dpi=300)
    ax.set_xlim(0, 155)
    ax.set_ylim(0, 72)
    ax.axis('off')

    # Color Palette matching reference image exactly
    # Reference blue: light pastel blue fill with medium blue outline
    c_blue_fill = '#cbe4f9'
    c_blue_edge = '#4184c4'
    
    # Reference grey: soft warm grey fill with darker grey outline
    c_gray_fill = '#e6e6e6'
    c_gray_edge = '#8f8f8f'
    
    # Reference green: pastel mint green fill with leafy green outline
    c_green_fill = '#cff2cb'
    c_green_edge = '#4ea349'
    c_green_cont_fill = '#eaf7e8'
    c_green_cont_edge = '#4ea349'
    
    # Loss coral box
    c_coral_fill = '#fadbd8'
    c_coral_edge = '#cb4335'
    
    # Thick arrow blue
    c_thick_blue = '#0b66c2'
    c_arrow_gray = '#68737d'
    c_arrow_green = '#388e3c'
    
    text_color = '#1f2937'

    def draw_box(x, y, w, h, fill, edge, lines, title_bold=True, rad=2.2, lw=1.8):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0.2,rounding_size={rad}',
                                      facecolor=fill, edgecolor=edge, linewidth=lw, zorder=3)
        ax.add_patch(rect)
        n_lines = len(lines)
        line_spacing = 2.6 if n_lines > 4 else 3.2
        total_h = (n_lines - 1) * line_spacing
        start_y = y + h/2 + total_h/2
        for i, line in enumerate(lines):
            is_bold = (i == 0 and title_bold)
            fs = 9.0 if is_bold else 8.0
            fw = 'bold' if is_bold else 'normal'
            ax.text(x + w/2, start_y - i * line_spacing, line,
                    ha='center', va='center', fontsize=fs, fontweight=fw,
                    color=text_color, zorder=5)

    def draw_cylinder(x, y, w, h, fill, edge, lines, lw=1.8):
        # Cylinder body with curved bottom
        ry = h * 0.15 # ellipse vertical radius
        
        # Draw bottom half-ellipse filled
        bot_ellipse = patches.Ellipse((x + w/2, y + ry), w, ry * 2,
                                      facecolor=fill, edgecolor=edge, lw=lw, zorder=2)
        ax.add_patch(bot_ellipse)
        
        # Rectangular middle body
        rect = patches.Rectangle((x, y + ry), w, h - 2 * ry,
                                 facecolor=fill, edgecolor='none', zorder=2)
        ax.add_patch(rect)
        
        # Left & Right straight borders
        ax.plot([x, x], [y + ry, y + h - ry], color=edge, lw=lw, zorder=4)
        ax.plot([x + w, x + w], [y + ry, y + h - ry], color=edge, lw=lw, zorder=4)
        
        # Re-stroke bottom arc
        bot_arc = patches.Arc((x + w/2, y + ry), w, ry * 2, theta1=180, theta2=360,
                              edgecolor=edge, lw=lw, zorder=4)
        ax.add_patch(bot_arc)
        
        # Top full ellipse
        top_ellipse = patches.Ellipse((x + w/2, y + h - ry), w, ry * 2,
                                      facecolor=fill, edgecolor=edge, lw=lw, zorder=4)
        ax.add_patch(top_ellipse)
        
        # Dashed middle band for 3D cylinder effect
        mid_y = y + (h - ry) * 0.45
        mid_arc = patches.Arc((x + w/2, mid_y), w, ry * 1.8, theta1=180, theta2=360,
                              edgecolor=edge, linestyle='--', lw=0.9, zorder=4)
        ax.add_patch(mid_arc)
        
        n_lines = len(lines)
        line_spacing = 2.5
        total_h = (n_lines - 1) * line_spacing
        start_y = y + (h - ry)/2 + total_h/2 - 0.5
        for i, line in enumerate(lines):
            is_bold = (i == 0)
            fs = 8.2 if is_bold else 7.4
            fw = 'bold' if is_bold else 'normal'
            ax.text(x + w/2, start_y - i * line_spacing, line,
                    ha='center', va='center', fontsize=fs, fontweight=fw,
                    color=text_color, zorder=5)

    def draw_thin_arrow(x1, y1, x2, y2, color=c_arrow_gray, label=None, label_above=True, lw=1.8):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->,head_width=0.45,head_length=0.65',
                                    color=color, lw=lw), zorder=4)
        if label:
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            dy = 1.6 if label_above else -1.6
            ax.text(mx, my + dy, label, ha='center', va='center', fontsize=7.2,
                    color='#374151', style='italic', zorder=6)

    def draw_thick_arrow(x1, y1, x2, y2, color=c_thick_blue, label=None, label_above=True):
        dx = x2 - x1
        shaft_h = 1.3
        head_l = 3.0
        head_w = 3.4
        
        shaft_len = dx - head_l
        points = [
            (x1, y1 - shaft_h/2),
            (x1 + shaft_len, y1 - shaft_h/2),
            (x1 + shaft_len, y1 - head_w/2),
            (x2, y1),
            (x1 + shaft_len, y1 + head_w/2),
            (x1 + shaft_len, y1 + shaft_h/2),
            (x1, y1 + shaft_h/2)
        ]
        arrow_poly = patches.Polygon(points, closed=True, facecolor=color, edgecolor=color, zorder=5)
        ax.add_patch(arrow_poly)
        
        if label:
            mx = (x1 + x2) / 2
            dy = 2.4 if label_above else -2.4
            ax.text(mx, y1 + dy, label, ha='center', va='center', fontsize=7.5,
                    color=color, fontweight='bold', zorder=6)

    # Title at the top center
    ax.text(77.5, 67, 'Ocular Disease Analysis System Architecture',
            ha='center', va='center', fontsize=16, fontweight='bold', color='#1e293b')

    # ==================== COORDINATE DEFINITIONS ====================
    # Y baseline for central horizontal flow
    y_center = 36.0
    
    # 1. Top-Left Box: Patient Fundus Scan (Blue)
    draw_box(4, 49, 15, 12.5, c_blue_fill, c_blue_edge,
             ['Patient Fundus', 'Color Scan', '(Input Image)'])

    # 2. Top-Mid-Left Box: Otsu Retinal FOV Segmentation (Grey)
    draw_box(25, 49, 18, 12.5, c_gray_fill, c_gray_edge,
             ['Otsu Retinal FOV', 'Segmentation', '& Morphology'])

    # 3. Mid-Left Box: Gabor Vessel Filtering (Grey)
    draw_box(4, 29, 17, 13, c_gray_fill, c_gray_edge,
             ['Gabor Filter Bank', '(Vessel & Texture', 'Enhancement)'])

    # 4. Bottom-Left Database: Ocular Image Dataset (Blue Cylinder)
    draw_cylinder(25, 7, 18, 18, c_blue_fill, c_blue_edge,
                  ['Ocular Image', 'Database', '(9,290 Images)', '5 Pathologies'])

    # 5. Central Hub: Retinal ROI & CLAHE Normalization (Light Blue)
    draw_box(27.5, 30.5, 13, 11, c_blue_fill, c_blue_edge,
             ['Retinal ROI', '& CLAHE', 'Norm (260×260)'])

    # 6. Reranker analog: Data Augmentation Engine (Grey)
    draw_box(49, 29, 17, 14, c_gray_fill, c_gray_edge,
             ['Data Augmentation', '& Normalization', '• Random Flips', '• Rotation & Jitter'])

    # 7. Prompt Assembly analog: EfficientNet-Lite2 Container (Green Box)
    cont_x, cont_y, cont_w, cont_h = 74, 20.5, 20, 31
    cont_rect = patches.FancyBboxPatch((cont_x, cont_y), cont_w, cont_h,
                                      boxstyle='round,pad=0.2,rounding_size=2.4',
                                      facecolor=c_green_cont_fill, edgecolor=c_green_cont_edge,
                                      linewidth=2.0, zorder=2)
    ax.add_patch(cont_rect)
    ax.text(cont_x + cont_w/2, cont_y + cont_h - 3.2, 'EfficientNet-Lite2',
            ha='center', va='center', fontsize=10, fontweight='bold', color=c_green_edge, zorder=4)

    # Two stacked sub-boxes inside container
    draw_box(cont_x + 1.8, cont_y + 14.5, 16.4, 10, c_green_fill, c_green_edge,
             ['MBConv Blocks', '(Inverted Res, ReLU6)'], rad=1.5, lw=1.2)
    draw_box(cont_x + 1.8, cont_y + 2.5, 16.4, 9.5, c_green_fill, c_green_edge,
             ['Global Average', 'Pooling (1280-d)'], rad=1.5, lw=1.2)

    # 8. LLM analog: Classification Head (Green)
    draw_box(102, 29.5, 18, 13, c_green_fill, c_green_edge,
             ['Linear Head', '& Softmax Triage', '(1280 → 5 Logits)'])

    # 9. Citation Grounding analog: Multiclass Focal Loss (Coral Box below LLM)
    draw_box(102, 10.0, 18, 12.5, c_coral_fill, c_coral_edge,
             ['Multiclass Focal Loss', '(α = 0.25, γ = 2.0)', '+ Class Balancing'])

    # 10. Final Answer Output analog: Diagnostic Output (Blue Box)
    draw_box(127.5, 25.5, 23.5, 21, c_blue_fill, c_blue_edge,
             ['Diagnostic Output', '5-Class Predictions:',
              '• Cataract: 97.8%', '• AMD: 96.0%', '• Glaucoma: 90.3%',
              '• Normal: 80.9%', '• DR: 80.1%'],
             title_bold=True, rad=2.4, lw=2.0)

    # ==================== CONNECTING ARROWS ====================

    # Arrow 1: Patient Fundus Scan -> Otsu Retinal FOV (Horizontal grey)
    draw_thin_arrow(19, 55.25, 25, 55.25, color=c_arrow_gray)

    # Arrow 2: Otsu Retinal FOV -> Retinal ROI & CLAHE (Slanted down to hub)
    draw_thin_arrow(34, 49, 34, 41.5, color=c_arrow_gray, label='FOV Mask', label_above=False)

    # Arrow 3: Gabor Filter Bank -> Retinal ROI & CLAHE (Horizontal grey)
    draw_thin_arrow(21, 35.5, 27.5, 35.5, color=c_arrow_gray)

    # Arrow 4: L-shaped arrow from Gabor Filter Bank -> Database (Indexing/Filtering)
    # Going down from bottom of Gabor Filter (x=12.5, y=29) down to y=16.5, then right to Database (x=25, y=16.5)
    ax.plot([12.5, 12.5], [29, 16.5], color=c_arrow_gray, lw=1.8, zorder=3)
    ax.annotate('', xy=(25, 16.5), xytext=(12.5, 16.5),
                arrowprops=dict(arrowstyle='->,head_width=0.45,head_length=0.65',
                                color=c_arrow_gray, lw=1.8), zorder=4)

    # Arrow 5: Database Cylinder -> Retinal ROI & CLAHE (Straight UP)
    draw_thin_arrow(34, 25, 34, 30.5, color=c_arrow_gray, label='Raw Fundus', label_above=False)

    # Arrow 6: Retinal ROI & CLAHE -> Data Augmentation (Horizontal grey)
    draw_thin_arrow(40.5, 36.0, 49, 36.0, color=c_arrow_gray, label='ROIs', label_above=True)

    # Arrow 7: Data Augmentation -> EfficientNet Container (THICK BLUE ARROW!)
    draw_thick_arrow(66, 36.0, 74, 36.0, color=c_thick_blue)

    # Internal arrow inside Container: MBConv -> Global Pooling
    draw_thin_arrow(cont_x + cont_w/2, cont_y + 14.5, cont_x + cont_w/2, cont_y + 12.0, color=c_arrow_green)

    # Arrow 8: EfficientNet Container -> Linear Head (Green horizontal arrow)
    draw_thin_arrow(cont_x + cont_w, 36.0, 102, 36.0, color=c_arrow_green, label='1280-d Latent', label_above=True)

    # Arrow 9: Linear Head <-> Multiclass Focal Loss (Vertical double arrow)
    ax.annotate('', xy=(111, 29.5), xytext=(111, 22.5),
                arrowprops=dict(arrowstyle='<->,head_width=0.45,head_length=0.65',
                                color=c_coral_edge, lw=1.8), zorder=4)
    ax.text(114.5, 26.0, 'Loss & Gradients', ha='left', va='center', fontsize=6.8,
            color=c_coral_edge, style='italic', zorder=6)

    # Arrow 10: Linear Head -> Diagnostic Output (THICK BLUE ARROW!)
    draw_thick_arrow(120, 36.0, 127.5, 36.0, color=c_thick_blue, label='Predicted Class', label_above=True)

    plt.tight_layout()
    out_path = 'scratch/system_architecture_rag_style.png'
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Successfully generated {out_path}!")

if __name__ == '__main__':
    create_system_architecture()
