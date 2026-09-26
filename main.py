import nextcord
from nextcord.ext import commands
import datetime

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

ROLE_ID = 1553228040719564912

class EliteRoleView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="🛡️ กดเพื่อรับ / ถอดถอนยศพิเศษ",
        style=nextcord.ButtonStyle.blurple,
        custom_id="elite_persistent_role_button"
    )
    async def toggle_role_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        role = interaction.guild.get_role(ROLE_ID)
        
        if not role:
            embed_err = nextcord.Embed(
                title="❌ เกิดข้อผิดพลาด",
                description="ไม่พบยศดังกล่าวในระบบเซิร์ฟเวอร์ กรุณาติดต่อผู้ดูแลระบบ",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=embed_err, ephemeral=True)
            return

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed_rem = nextcord.Embed(
                title="🗑️ ถอดถอนบทบาทสำเร็จ",
                description=f"นำยศ **{role.name}** ออกจากตัวคุณเรียบร้อยแล้ว",
                color=nextcord.Color.orange()
            )
            embed_rem.set_footer(text=f"ทำรายการโดย: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed_rem, ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            embed_add = nextcord.Embed(
                title="🎉 รับบทบาทสำเร็จ!",
                description=f"คุณได้รับยศ **{role.name}** เรียบร้อยแล้ว ขอให้สนุกกับโซนใหม่!",
                color=nextcord.Color.green()
            )
            embed_add.set_footer(text=f"ทำรายการโดย: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed_add, ephemeral=True)

@bot.event
async def on_ready():
    bot.add_view(EliteRoleView())
    print("========================================")
    print(f"🔥 Bot Logged in as: {bot.user.name} ({bot.user.id})")
    print("🚀 Status: Online & Ready for Action!")
    print("========================================")
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="!help | ระบบสุดอลังการ"))

@bot.command(name="help")
async def help_command(ctx):
    embed = nextcord.Embed(
        title="🌟 ศูนย์รวมคำสั่งขั้นเทพ (Command Center)",
        description="รายการคำสั่งทั้งหมดที่บอทตัวนี้รองรับ ออกแบบมาเพื่อความสะดวกและเสถียรสูงสุด",
        color=nextcord.Color.from_rgb(88, 101, 242)
    )
    embed.add_field(name="✨ `!sendrole`", value="ส่งแผงควบคุมปุ่มกดรับยศสุดหรู (Admin Only)", inline=False)
    embed.add_field(name="👤 `!whois [@User]`", value="เช็คข้อมูลเชิงลึกของผู้ใช้งานในเซิร์ฟเวอร์", inline=False)
    embed.add_field(name="📊 `!server`", value="แสดงสถิติและข้อมูลภาพรวมของเซิร์ฟเวอร์", inline=False)
    embed.add_field(name="🧹 `!clear [จำนวน]`", value="เคลียร์ข้อความแชทอย่างรวดเร็ว (Admin Only)", inline=False)
    
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    embed.set_footer(text=f"เรียกใช้งานโดย {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
    embed.timestamp = datetime.datetime.now()
    await ctx.send(embed=embed)

@bot.command(name="sendrole")
@commands.has_permissions(administrator=True)
async def sendrole(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    
    embed = nextcord.Embed(
        title="⚡ ระบบลงทะเบียนรับยศอัตโนมัติ (Role Verification)",
        description="กดปุ่มด้านล่างเพื่อรับหรือยกเลิกยศพิเศษภายในเซิร์ฟเวอร์\nระบบจะทำการอัปเดตยศให้คุณทันทีแบบ Real-time!",
        color=nextcord.Color.gold()
    )
    embed.add_field(name="📌 คำแนะนำ", value="• กด 1 ครั้งเพื่อรับยศ\n• กดซ้ำอีกครั้งเพื่อถอดถอนยศออก", inline=False)
    embed.set_footer(text="ระบบรักษาความปลอดภัยเซิร์ฟเวอร์ระดับสูง", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
    
    await ctx.send(embed=embed, view=EliteRoleView())

@bot.command(name="whois")
async def whois(ctx, member: nextcord.Member = None):
    member = member or ctx.author
    roles = [role.mention for role in member.roles[1:]]
    roles_str = ", ".join(roles) if roles else "ไม่มีบทบาทพิเศษ"

    embed = nextcord.Embed(title=f"👤 ข้อมูลผู้ใช้งาน: {member.name}", color=member.color)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="🆔 User ID", value=member.id, inline=True)
    embed.add_field(name="🏷️ ชื่อเล่นในเซิร์ฟ", value=member.display_name, inline=True)
    embed.add_field(name="📅 วันที่เข้าสู่เซิร์ฟเวอร์", value=member.joined_at.strftime("%d/%m/%Y %H:%M"), inline=False)
    embed.add_field(name="📅 วันที่สร้างบัญชี Discord", value=member.created_at.strftime("%d/%m/%Y %H:%M"), inline=False)
    embed.add_field(name=f"🎭 บทบาททั้งหมด ({len(member.roles)-1})", value=roles_str, inline=False)
    
    embed.set_footer(text=f"เรียกข้อมูลโดย {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="server")
async def server_info(ctx):
    guild = ctx.guild
    embed = nextcord.Embed(title=f"📊 ข้อมูลเชิงลึกของเซิร์ฟเวอร์: {guild.name}", color=nextcord.Color.purple())
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
        
    embed.add_field(name="👑 เจ้าของเซิร์ฟเวอร์", value=guild.owner.mention, inline=True)
    embed.add_field(name="🆔 Server ID", value=guild.id, inline=True)
    embed.add_field(name="👥 สมาชิกทั้งหมด", value=f"{guild.member_count} คน", inline=True)
    embed.add_field(name="🔒 ระดับความปลอดภัย", value=str(guild.verification_level).title(), inline=True)
    embed.add_field(name="💬 จำนวนช่องแชท/ห้อง", value=f"{len(guild.channels)} ห้อง", inline=True)
    embed.add_field(name="🛡️ จำนวนยศทั้งหมด", value=f"{len(guild.roles)} ยศ", inline=True)
    
    embed.set_footer(text=f"สร้างเมื่อ: {guild.created_at.strftime('%d/%m/%Y')}", icon_url=guild.icon.url if guild.icon else None)
    await ctx.send(embed=embed)

@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    if amount < 1:
        await ctx.send("❌ กรุณาระบุจำนวนมากกว่า 0", delete_after=5)
        return
    deleted = await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 ทำการลบข้อความออกไป **{len(deleted)-1}** ข้อความเรียบร้อยแล้ว!")
    await msg.delete(delay=4)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ **[Access Denied]** คุณไม่มีสิทธิ์เพียงพอในการใช้คำสั่งนี้!", delete_after=6)
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        print(f"⚠️ เกิดข้อผิดพลาด: {error}")

bot.run("MTU1MDQ5MjQ5NjYyMDk0NTQwOA.GPKAp9.in9fnbAkgH-OPgZ4iEcd2jGw3Zb6FGHIdPio6U")
  
